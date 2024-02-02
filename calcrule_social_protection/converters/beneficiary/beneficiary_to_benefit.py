from calcrule_social_protection.converters.builder import BuilderToBenefitConverter
from calcrule_social_protection.utils import generate_unique_code
from calcrule_social_protection.apps import CalcruleSocialProtectionConfig


class BeneficiaryToBenefitConverter(BuilderToBenefitConverter):

    @classmethod
    def _build_individual(cls, benefit, entity):
        benefit["individual"] = entity.individual

    @classmethod
    def _build_code(cls, benefit):
        unique_code = generate_unique_code(CalcruleSocialProtectionConfig.code_length)
        benefit["code"] = unique_code
