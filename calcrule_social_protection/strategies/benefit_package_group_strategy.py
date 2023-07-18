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
        amount = kwargs.get('amount', None)
        convert_results = cls._convert_group_to_bill(payment_plan, group, amount)
        convert_results['user'] = kwargs.get('user', None)
        result_bill_creation = BillService.bill_create(convert_results=convert_results)
        return result_bill_creation

    @classmethod
    def _convert_group_to_bill(cls, payment_plan, group, amount):
        bill = GroupToBillConverter.to_bill_obj(
            payment_plan, group, amount
        )
        bill_line_items = [
            GroupToBillItemConverter.to_bill_item_obj(payment_plan, group, amount)
        ]
        return {
            'bill_data': bill,
            'bill_data_line': bill_line_items,
            'type_conversion': 'group - bill'
        }