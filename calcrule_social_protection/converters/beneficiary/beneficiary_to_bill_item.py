from calcrule_social_protection.converters.builder import BuilderToBillItemConverter


class BeneficiaryToBillItemConverter(BuilderToBillItemConverter):

    @classmethod
    def _build_code(cls, bill_line_item, beneficiary):
        bill_line_item["code"] = f"{beneficiary.individual.first_name}-{beneficiary.individual.last_name}"
