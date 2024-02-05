from calcrule_social_protection.converters.builder import BuilderToBenefitConverter


class BeneficiaryToBenefitConverter(BuilderToBenefitConverter):

    @classmethod
    def _build_individual(cls, benefit, entity):
        benefit["individual_id"] = f"{entity.individual.id}"
