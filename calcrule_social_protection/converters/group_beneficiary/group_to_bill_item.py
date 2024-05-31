from calcrule_social_protection.converters.builder import BuilderToBillItemConverter


class GroupToBillItemConverter(BuilderToBillItemConverter):

    @classmethod
    def _build_code(cls, bill_line_item, group):
        bill_line_item["code"] = f"{group.group.code}"
