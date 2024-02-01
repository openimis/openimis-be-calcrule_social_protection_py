from payroll.models import BenefitConsumption, BenefitConsumptionStatus
from invoice.models import Bill


class BuilderToBenefitConverter:
    TYPE = None

    @classmethod
    def to_benefit_obj(cls, entity, amount, payment_plan):
        benefit = {}
        cls._build_individual(benefit, entity)
        cls._build_code(benefit, entity, payment_plan)
        cls._build_receipt(benefit, entity, payment_plan)
        cls._build_amount(benefit, amount)
        cls._build_date_dates(benefit, payment_plan)
        cls._build_type(benefit)
        cls._build_status(benefit)
        return benefit

    @classmethod
    def _build_individual(cls, benefit, entity):
        pass

    @classmethod
    def _build_code(cls, benefit, entity, payment_plan):
        pass

    @classmethod
    def _build_receipt(cls, benefit, entity, payment_plan):
        """"
        individual = beneficiary.individual
        benefit_plan = payment_plan.benefit_plan
        benefit["receipt"] = f"{benefit_plan.code}-{individual.first_name}-{individual.last_name}"
        """
        pass

    @classmethod
    def _build_amount(cls, benefit, amount):
        benefit["amount"] = amount

    @classmethod
    def _build_date_dates(cls, benefit, payment_plan):
        from core import datetime, datetimedelta
        benefit["date_due"] = f"{datetime.date.today() + datetimedelta(days=30)}"
        benefit["date_valid_from"] = f"{ payment_plan.benefit_plan.date_valid_from}"
        benefit["date_valid_to"] = f"{payment_plan.benefit_plan.date_valid_to}"

    @classmethod
    def _build_type(cls, benefit):
        benefit["type"] = 'Cash Transfer'

    @classmethod
    def _build_status(cls, benefit):
        benefit["status"] = BenefitConsumptionStatus.ACCEPTED.value
