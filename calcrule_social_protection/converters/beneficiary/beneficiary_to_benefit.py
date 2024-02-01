from calcrule_social_protection.converters.builder import BuilderToBenefitConverter


class BeneficiaryToBenefitConverter(BuilderToBenefitConverter):

    @classmethod
    def _build_individual(cls, benefit, entity):
        benefit["individual"] = entity.individual

    @classmethod
    def _build_code(cls, benefit, entity, payment_plan):
        individual = entity.individual
        benefit_plan = payment_plan.benefit_plan
        benefit["receipt"] = f"{benefit_plan.code}-{individual.first_name}-{individual.last_name}"

    @classmethod
    def _build_receipt(cls, benefit, entity, payment_plan):
        individual = entity.individual
        benefit_plan = payment_plan.benefit_plan
        benefit["receipt"] = f"{benefit_plan.code}-{individual.first_name}-{individual.last_name}"
