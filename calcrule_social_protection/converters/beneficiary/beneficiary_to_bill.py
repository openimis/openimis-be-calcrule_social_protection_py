from calcrule_social_protection.converters.builder import BuilderToBillConverter


class BeneficiaryToBillConverter(BuilderToBillConverter):

    @classmethod
    def _build_terms(cls, bill, payment_plan, beneficiary, end_date):
        bill["terms"] = f"{payment_plan.benefit_plan.code}-{end_date}: " \
                       f"{beneficiary.individual.first_name}-{beneficiary.individual.last_name}"
