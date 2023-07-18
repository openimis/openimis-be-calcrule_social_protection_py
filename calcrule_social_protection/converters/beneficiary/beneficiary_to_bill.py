from calcrule_social_protection.converters.base import BaseBenefitPackageStrategyConverter


class BeneficiaryToBillConverter(BaseBenefitPackageStrategyConverter):

    @classmethod
    def _build_code(cls, bill, payment_plan, beneficiary):
        from core import datetime
        date = datetime.date.today()
        bill["code"] = f"{payment_plan.benefit_plan.code}-{date}: " \
                       f"{beneficiary.individual.first_name} {beneficiary.individual.last_name}"

