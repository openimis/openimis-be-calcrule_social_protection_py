from calcrule_social_protection.converters.base import BaseBenefitPackageStrategyItemConverter


class GroupToBillItemConverter(BaseBenefitPackageStrategyItemConverter):

    @classmethod
    def _build_code(cls, bill_line_item, group):
        bill_line_item["code"] = f"{group.id}"
