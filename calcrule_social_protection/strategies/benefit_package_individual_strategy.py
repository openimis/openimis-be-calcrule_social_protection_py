from invoice.services import BillService
from social_protection.models import Beneficiary
from calcrule_social_protection.converters import (
    BeneficiaryToBillConverter,
    BeneficiaryToBillItemConverter
)
from calcrule_social_protection.strategies.benefit_package_base_strategy import BaseBenefitPackageStrategy


class IndividualBenefitPackageStrategy(BaseBenefitPackageStrategy):
    TYPE = "INDIVIDUAL"
    BENEFICIARY_OBJECT = Beneficiary
    BENEFICIARY_TYPE = "beneficiary"

    @classmethod
    def convert(cls, payment_plan, **kwargs):
        beneficiary = kwargs.get('beneficiary', None)
        # super().convert(payment_plan, beneficiary=beneficiary, **kwargs)
        amount = kwargs.get('amount', None)
        convert_results = cls._convert_beneficiary_to_bill(payment_plan, beneficiary, amount)
        convert_results['user'] = kwargs.get('user', None)
        result_bill_creation = BillService.bill_create(convert_results=convert_results)
        return result_bill_creation

    @classmethod
    def _convert_beneficiary_to_bill(cls, payment_plan, beneficiary, amount):
        bill = BeneficiaryToBillConverter.to_bill_obj(
            payment_plan, beneficiary, amount
        )
        bill_line_items = [
            BeneficiaryToBillItemConverter.to_bill_item_obj(payment_plan, beneficiary, amount)
        ]
        return {
            'bill_data': bill,
            'bill_data_line': bill_line_items,
            'type_conversion': 'beneficiary - bill'
        }
