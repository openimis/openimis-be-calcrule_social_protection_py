from core.models import User
from invoice.services import BillService
from social_protection.models import GroupBeneficiary

from calcrule_social_protection.converters import (
    GroupToBillConverter,
    GroupToBillItemConverter
)


class GroupBenefitPlanInterface:
    TYPE = "GROUP"

    @classmethod
    def check_calculation(cls, calculation, payment_plan):
        return calculation.uuid == str(payment_plan.calculation)

    @classmethod
    def calculate(cls, calculation, payment_plan, **kwargs):
        # 1. Get the list of beneficiares assigned to benefit plan from payment plan
        # each beneficiary group from benefit plan assigned to this payment plan is a single bill
        groups_beneficiary = GroupBeneficiary.objects.filter(benefit_plan=payment_plan.benefit_plan)
        # 2. Get the parameters from payment plan with fixed and advanced criteria
        payment_plan_parameters = payment_plan.json_ext
        audit_user_id, start_date, end_date = \
            calculation.get_payment_cycle_parameters(**kwargs)
        user = User.objects.filter(i_user__id=audit_user_id).first()
        for group_beneficiary in groups_beneficiary:
            # TODO add calculation mechanism once is developed as a part of CM-210
            #  ticket - at this stage use fixed amount
            fixed_amount = payment_plan_parameters['calculation_rule']['fixed_batch']
            calculation.run_convert(
                payment_plan,
                group=group_beneficiary.group,
                amount=fixed_amount,
                user=user
            )
        return "calculation and tranformation into bills finished successfully"

    @classmethod
    def convert(cls, payment_plan, **kwargs):
        group = kwargs.get('group', None)
        amount = kwargs.get('amount', None)
        convert_results = cls._convert_group_to_bill(payment_plan, group, amount)
        convert_results['user'] = kwargs.get('user', None)
        result_bill_creation = BillService.bill_create(convert_results=convert_results)
        return result_bill_creation

    @classmethod
    def _convert_group_to_bill(cls, payment_plan, group, amount):
        bill = GroupToBillConverter.to_bill_obj(
            payment_plan, group, amount
        )
        bill_line_items = [
            GroupToBillItemConverter.to_bill_item_obj(payment_plan, group, amount)
        ]
        return {
            'bill_data': bill,
            'bill_data_line': bill_line_items,
            'type_conversion': 'group - bill'
        }