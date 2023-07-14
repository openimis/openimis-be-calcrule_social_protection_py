from core.abs_calculation_rule import AbsCalculationRule

from calcrule_social_protection.interfaces import (
    GroupBenefitPlanInterface,
    IndividualBenefitPlanInterface
)


class BenefitPackageStrategy(AbsCalculationRule):

    @classmethod
    def run_calculation_rules(cls, sender, payment_plan, user, context, **kwargs):
        return cls.calculate_if_active_for_object(payment_plan, **kwargs)

    @classmethod
    def calculate_if_active_for_object(cls, payment_plan, **kwargs):
        if cls.active_for_object(payment_plan):
            return cls.calculate(payment_plan, **kwargs)

    @classmethod
    def active_for_object(cls, payment_plan):
        return cls.check_calculation(payment_plan)

    @classmethod
    def get_linked_class(cls, sender, class_name, **kwargs):
        return ["Calculation"]

    @classmethod
    def run_convert(cls, payment_plan, **kwargs):
        return cls.convert(payment_plan=payment_plan, **kwargs)

    @classmethod
    def check_calculation(cls, payment_plan, **kwargs):
        benefit_plan_type = payment_plan.benefit_plan.type
        if benefit_plan_type == GroupBenefitPlanInterface.TYPE:
            return GroupBenefitPlanInterface.check_calculation(cls, payment_plan)
        if benefit_plan_type == IndividualBenefitPlanInterface.TYPE:
            return IndividualBenefitPlanInterface.check_calculation(cls, payment_plan)

    @classmethod
    def calculate(cls, payment_plan, **kwargs):
        benefit_plan_type = payment_plan.benefit_plan.type
        if benefit_plan_type == GroupBenefitPlanInterface.TYPE:
            GroupBenefitPlanInterface.calculate(cls, payment_plan, **kwargs)
        if benefit_plan_type == IndividualBenefitPlanInterface.TYPE:
            IndividualBenefitPlanInterface.calculate(cls, payment_plan, **kwargs)

    @classmethod
    def convert(cls, payment_plan, **kwargs):
        benefit_plan_type = payment_plan.benefit_plan.type
        if benefit_plan_type == GroupBenefitPlanInterface.TYPE:
            GroupBenefitPlanInterface.convert(payment_plan, **kwargs)
        if benefit_plan_type == IndividualBenefitPlanInterface.TYPE:
            IndividualBenefitPlanInterface.convert(payment_plan, **kwargs)

    @classmethod
    def get_payment_cycle_parameters(cls, **kwargs):
        audit_user_id = kwargs.get('audit_user_id', None)
        start_date = kwargs.get('start_date', None)
        end_date = kwargs.get('end_date', None)
        return audit_user_id, start_date, end_date
