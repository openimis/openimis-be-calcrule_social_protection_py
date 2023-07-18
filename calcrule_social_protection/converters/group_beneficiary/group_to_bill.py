from calcrule_social_protection.converters.base import BaseBenefitPackageStrategyConverter


class GroupToBillConverter(BaseBenefitPackageStrategyConverter):

    @classmethod
    def _build_code(cls, bill, payment_plan, group):
        from core import datetime
        date = datetime.date.today()
        bill["code"] = f"{payment_plan.benefit_plan.code}-{date}: " \
                       f"{group.id}"
