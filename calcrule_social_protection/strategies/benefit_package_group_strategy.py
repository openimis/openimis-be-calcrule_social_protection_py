from invoice.services import BillService
from social_protection.models import GroupBeneficiary

from calcrule_social_protection.converters import (
    GroupToBillConverter,
    GroupToBillItemConverter
)
from calcrule_social_protection.strategies.benefit_package_base_strategy import BaseBenefitPackageStrategy


class GroupBenefitPackageStrategy(BaseBenefitPackageStrategy):
    TYPE = "GROUP"
    BENEFICIARY_OBJECT = GroupBeneficiary
    BENEFICIARY_TYPE = "group"

    @classmethod
    def convert(cls, payment_plan, **kwargs):
        group = kwargs.get('group', None)
        additional_parameters = {
            "entity": group,
            "converter": GroupToBillConverter,
            "converter_item": GroupToBillItemConverter,
            **kwargs
        }
        return super().convert(payment_plan, **additional_parameters)
