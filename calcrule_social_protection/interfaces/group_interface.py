from core.models import User
from social_protection.models import GroupBeneficiary


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
                group=group_beneficiary,
                amount=fixed_amount,
                user=user
            )
        return "calculation and tranformation into bills finished successfully"

    @classmethod
    def convert(cls, calculation, payment_plan, convert_to, **kwargs):
        pass