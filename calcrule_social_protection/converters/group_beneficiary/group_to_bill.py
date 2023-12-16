from calcrule_social_protection.converters.builder import BuilderToBillConverter


class GroupToBillConverter(BuilderToBillConverter):

    @classmethod
    def _build_code(cls, bill, payment_plan, group, end_date):
        bill["code"] = f"{payment_plan.benefit_plan.code}-{end_date.date()}: " \
                       f"{group.id}"
