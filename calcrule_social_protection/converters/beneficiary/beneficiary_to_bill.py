from calcrule_social_protection.converters.builder import BuilderToBillConverter


class BeneficiaryToBillConverter(BuilderToBillConverter):

    @classmethod
    def _build_code(cls, bill, payment_plan, beneficiary, end_date):
        bill["code"] = f"{payment_plan.benefit_plan.code}-{end_date.date()}: " \
                       f"{beneficiary.id}-{beneficiary.individual.first_name}-{beneficiary.individual.last_name}"
