from django.db import transaction

from calcrule_social_protection.apps import CalcruleSocialProtectionConfig
from core.models import User
from core.utils import convert_to_python_value
from core.signals import register_service_signal
from invoice.models import Bill
from invoice.services import BillService
from social_protection.models import BeneficiaryStatus
from tasks_management.apps import TasksManagementConfig
from tasks_management.models import Task
from tasks_management.services import TaskService

from calcrule_social_protection.strategies.benefit_package_strategy_interface import BenefitPackageStrategyInterface


class BaseBenefitPackageStrategy(BenefitPackageStrategyInterface):
    is_exceed_limit = False

    @classmethod
    def check_calculation(cls, calculation, payment_plan):
        return calculation.uuid == str(payment_plan.calculation)

    @classmethod
    def calculate(cls, calculation, payment_plan, **kwargs):
        # 1. Get the list of beneficiares assigned to benefit plan from payment plan
        # each beneficiary group from benefit plan assigned to this payment plan is a single bill
        beneficiares = cls.BENEFICIARY_OBJECT.objects.filter(
            benefit_plan=payment_plan.benefit_plan, status=BeneficiaryStatus.ACTIVE
        )
        # 2. Get the parameters from payment plan with fixed and advanced criteria
        payment_plan_parameters = payment_plan.json_ext
        audit_user_id, start_date, end_date, payment_cycle = \
            calculation.get_payment_cycle_parameters(**kwargs)
        user = User.objects.filter(i_user__id=audit_user_id).first()
        payment = payment_plan_parameters['calculation_rule']['fixed_batch']
        limit = payment_plan_parameters['calculation_rule']['limit_per_single_transaction']
        advanced_filters_criteria = payment_plan_parameters['advanced_criteria'] if 'advanced_criteria' in payment_plan_parameters else []
        for beneficiary in beneficiares:
            calculated_payment = cls._calculate_payment(
                beneficiary, advanced_filters_criteria, payment, limit
            )

            additional_params = {
                f"{cls.BENEFICIARY_TYPE}": beneficiary,
                "amount": calculated_payment,
                "user": user,
                "end_date": end_date,
                "payment_cycle": payment_cycle
            }
            calculation.run_convert(
                payment_plan,
                **additional_params
            )
        return "Calculation and transformation into bills completed successfully."

    @classmethod
    def _calculate_payment(cls, beneficiary, advanced_filters_criteria, payment, limit):
        for criterion in advanced_filters_criteria:
            condition = criterion['custom_filter_condition']
            calculated_amount = float(criterion['amount'])
            if cls._does_beneficiary_meet_condition(beneficiary, condition):
                payment += calculated_amount
        cls.is_exceed_limit = True if payment > limit else False
        return payment

    @classmethod
    def _does_beneficiary_meet_condition(cls, beneficiary, condition):
        condition_key, condition_value = condition.split("=")
        json_key, lookup = condition_key.split('__')[0:2]
        parsed_condition_value = convert_to_python_value(condition_value)
        if json_key in beneficiary.json_ext:
            return cls.BENEFICIARY_OBJECT.objects.filter(
                        id=beneficiary.id, **{f'json_ext__{json_key}__{lookup}': parsed_condition_value}
                    ).exists()
        return False

    @classmethod
    def convert(cls, payment_plan, **kwargs):
        entity = kwargs.get('entity', None)
        amount = kwargs.get('amount', None)
        end_date = kwargs.get('end_date', None)
        payment_cycle = kwargs.get('payment_cycle', None)
        converter = kwargs.get('converter')
        converter_item = kwargs.get('converter_item')
        convert_results = cls._convert_entity_to_bill(
            converter, converter_item, payment_plan, entity, amount, end_date, payment_cycle
        )
        convert_results['user'] = kwargs.get('user', None)
        if not cls.is_exceed_limit:
            result_bill_creation = BillService.bill_create(convert_results=convert_results)
            return result_bill_creation
        else:
            cls.create_task_after_exceeding_limit(convert_results=convert_results)

    @classmethod
    def _convert_entity_to_bill(
        cls, converter, converter_item, payment_plan, entity, amount, end_date, payment_cycle
    ):
        bill = converter.to_bill_obj(
            payment_plan, entity, amount, end_date, payment_cycle
        )
        bill_line_items = [
            converter_item.to_bill_item_obj(payment_plan, entity, amount)
        ]
        return {
            'bill_data': bill,
            'bill_data_line': bill_line_items,
            'type_conversion': 'beneficiary - bill'
        }

    @classmethod
    @transaction.atomic
    @register_service_signal('calcrule_social_protection.create_task')
    def create_task_after_exceeding_limit(cls, convert_results):
        business_status = {"code": convert_results['bill_data']['code']}
        user = convert_results.pop('user')
        TaskService(user).create({
            'source': 'calcrule_social_protection',
            'entity': None,
            'status': Task.Status.RECEIVED,
            'executor_action_event': TasksManagementConfig.default_executor_event,
            'business_event': CalcruleSocialProtectionConfig.calculate_business_event,
            'business_status': business_status,
            'data': f"{convert_results}"
        })
