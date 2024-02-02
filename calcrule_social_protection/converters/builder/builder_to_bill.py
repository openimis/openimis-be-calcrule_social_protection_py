from django.contrib.contenttypes.models import ContentType
from invoice.apps import InvoiceConfig
from invoice.models import Bill
from calcrule_social_protection.utils import generate_unique_code
from calcrule_social_protection.apps import CalcruleSocialProtectionConfig


class BuilderToBillConverter:
    TYPE = None

    @classmethod
    def to_bill_obj(cls, payment_plan, entity, amount, end_date):
        bill = {}
        cls._build_subject(bill, entity)
        cls._build_thirdparty(bill, payment_plan)
        cls._build_code(bill)
        cls._build_price(bill, amount)
        cls._build_terms(bill, payment_plan, entity, end_date)
        cls._build_date_dates(bill, payment_plan)
        cls._build_currency(bill)
        cls._build_status(bill)
        return bill

    @classmethod
    def _build_subject(cls, bill, entity):
        bill["subject_id"] = f"{entity.id}"
        bill['subject_type_id'] = f"{ContentType.objects.get_for_model(entity).id}"

    @classmethod
    def _build_thirdparty(cls, bill, payment_plan):
        bill["thirdparty_id"] = f"{payment_plan.id}"
        bill['thirdparty_type_id'] = f"{ContentType.objects.get_for_model(payment_plan).id}"

    @classmethod
    def _build_code(cls, bill):
        bill["code"] = f"{generate_unique_code(CalcruleSocialProtectionConfig.code_length)}"

    @classmethod
    def _build_price(cls, bill, amount):
        bill["amount_net"] = amount

    @classmethod
    def _build_date_dates(cls, bill, payment_plan):
        from core import datetime, datetimedelta
        bill["date_due"] = f"{datetime.date.today() + datetimedelta(days=30)}"
        bill["date_bill"] = f"{datetime.date.today()}"
        bill["date_valid_from"] = f"{ payment_plan.benefit_plan.date_valid_from}"
        bill["date_valid_to"] = f"{payment_plan.benefit_plan.date_valid_to}"

    @classmethod
    def _build_currency(cls, bill):
        bill["currency_tp_code"] = InvoiceConfig.default_currency_code
        bill["currency_code"] = InvoiceConfig.default_currency_code

    @classmethod
    def _build_status(cls, bill):
        bill["status"] = Bill.Status.VALIDATED.value

    @classmethod
    def _build_terms(cls, bill, payment_plan, entity, end_date):
        pass
