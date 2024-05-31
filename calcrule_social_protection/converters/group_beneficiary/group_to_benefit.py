from calcrule_social_protection.converters.builder import BuilderToBenefitConverter
from individual.models import GroupIndividual


class GroupToBenefitConverter(BuilderToBenefitConverter):
    @classmethod
    def to_benefit_obj(cls, entity, amount, payment_plan, payment_cycle):
        group_head = GroupIndividual.objects.filter(
            group_id=entity.group.id,
            role=GroupIndividual.RecipientType.PRIMARY.value,
            is_deleted=False
        ).first()
        if group_head:
            return super().to_benefit_obj(group_head, amount, payment_plan, payment_cycle)
        else:
            group_head = GroupIndividual.objects.filter(
                group_id=entity.group.id,
                is_deleted=False
            ).first()
            return super().to_benefit_obj(group_head, amount, payment_plan, payment_cycle)

    @classmethod
    def _build_individual(cls, benefit, entity):
        benefit["individual_id"] = f"{entity.individual.id}"
