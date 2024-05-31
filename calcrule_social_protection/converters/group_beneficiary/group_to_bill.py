from calcrule_social_protection.converters.builder import BuilderToBillConverter


class GroupToBillConverter(BuilderToBillConverter):

    @classmethod
    def _build_terms(cls, bill, payment_plan, group, end_date):
        bill["terms"] = f"{payment_plan.benefit_plan.code}-{end_date}: " \
                       f"{group.group.code}"
