from calcrule_social_protection.utils import CodeGenerator
from calcrule_social_protection.apps import CalcruleSocialProtectionConfig
from payroll.models import BenefitConsumptionStatus


class BuilderToBenefitConverter:
    TYPE = None

    @classmethod
    def to_benefit_obj(cls, entity, amount, payment_plan, payment_cycle):
        benefit = {}
        cls._build_individual(benefit, entity)
        cls._build_code(benefit)
        cls._build_amount(benefit, amount)
        cls._build_date_dates(benefit, payment_plan, payment_cycle)
        cls._build_type(benefit)
        cls._build_status(benefit)
        return benefit

    @classmethod
    def _build_individual(cls, benefit, entity):
        pass

    @classmethod
    def _build_code(cls, benefit):
        code = CodeGenerator.generate_unique_code(
            'payroll',
            'BenefitConsumption',
            'code',
            CalcruleSocialProtectionConfig.code_length
        )
        benefit["code"] = code

    @classmethod
    def _build_amount(cls, benefit, amount):
        benefit["amount"] = amount

    @classmethod
    def _build_date_dates(cls, benefit, payment_plan, payment_cycle):
        benefit["date_due"] = f"{payment_cycle.end_date}"
        benefit["date_valid_from"] = f"{ payment_plan.benefit_plan.date_valid_from}"
        benefit["date_valid_to"] = f"{payment_plan.benefit_plan.date_valid_to}"

    @classmethod
    def _build_type(cls, benefit):
        benefit["type"] = 'Cash Transfer'

    @classmethod
    def _build_status(cls, benefit):
        benefit["status"] = BenefitConsumptionStatus.ACCEPTED.value
