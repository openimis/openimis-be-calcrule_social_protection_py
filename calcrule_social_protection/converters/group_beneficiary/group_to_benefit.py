from calcrule_social_protection.converters.builder import BuilderToBenefitConverter
from individual.models import GroupIndividual


class GroupToBenefitConverter(BuilderToBenefitConverter):
    @classmethod
    def to_benefit_obj(cls, entity, amount, payment_plan):
        group_head = GroupIndividual.objects.get(id=entity.id, role=GroupIndividual.Role.HEAD.value)
        return super().to_benefit_obj(group_head, amount, payment_plan)

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
