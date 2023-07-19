from core.models import User
from invoice.services import BillService
from social_protection.models import BeneficiaryStatus

from calcrule_social_protection.strategies.benefit_package_strategy_interface import BenefitPackageStrategyInterface


class BaseBenefitPackageStrategy(BenefitPackageStrategyInterface):
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
        audit_user_id, start_date, end_date = \
            calculation.get_payment_cycle_parameters(**kwargs)
        user = User.objects.filter(i_user__id=audit_user_id).first()
        for beneficiary in beneficiares:
            # TODO add calculation mechanism once is developed as a part of CM-210
            #  ticket - at this stage use fixed amount
            fixed_amount = payment_plan_parameters['calculation_rule']['fixed_batch']
            additional_params = {
                f"{cls.BENEFICIARY_TYPE}": beneficiary,
                "amount": fixed_amount,
                "user": user
            }
            calculation.run_convert(
                payment_plan,
                **additional_params
            )
        return "Calculation and transformation into bills completed successfully."

    @classmethod
    def convert(cls, payment_plan, **kwargs):
        entity = kwargs.get('entity', None)
        amount = kwargs.get('amount', None)
        converter = kwargs.get('converter')
        converter_item = kwargs.get('converter_item')
        convert_results = cls._convert_entity_to_bill(converter, converter_item, payment_plan, entity, amount)
        convert_results['user'] = kwargs.get('user', None)
        result_bill_creation = BillService.bill_create(convert_results=convert_results)
        return result_bill_creation

    @classmethod
    def _convert_entity_to_bill(cls, converter, converter_item, payment_plan, entity, amount):
        bill = converter.to_bill_obj(
            payment_plan, entity, amount
        )
        bill_line_items = [
            converter_item.to_bill_item_obj(payment_plan, entity, amount)
        ]
        return {
            'bill_data': bill,
            'bill_data_line': bill_line_items,
            'type_conversion': 'beneficiary - bill'
        }