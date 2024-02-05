from social_protection.models import Beneficiary
from calcrule_social_protection.converters import (
    BeneficiaryToBillConverter,
    BeneficiaryToBillItemConverter,
    BeneficiaryToBenefitConverter
)
from calcrule_social_protection.strategies.benefit_package_base_strategy import BaseBenefitPackageStrategy


class IndividualBenefitPackageStrategy(BaseBenefitPackageStrategy):
    TYPE = "INDIVIDUAL"
    BENEFICIARY_OBJECT = Beneficiary
    BENEFICIARY_TYPE = "beneficiary"

    @classmethod
    def convert(cls, payment_plan, **kwargs):
        beneficiary = kwargs.get('beneficiary', None)
        additional_parameters = {
            "entity": beneficiary,
            "converter": BeneficiaryToBillConverter,
            "converter_item": BeneficiaryToBillItemConverter,
            "converter_benefit": BeneficiaryToBenefitConverter,
            **kwargs
        }
        return super().convert(payment_plan, **additional_parameters)
