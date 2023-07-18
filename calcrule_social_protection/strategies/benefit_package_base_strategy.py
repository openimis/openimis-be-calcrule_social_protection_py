from core.models import User
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
