from django.contrib.contenttypes.models import ContentType

from invoice.apps import InvoiceConfig
from invoice.models import Bill


class BeneficiaryToBillConverter:

    @classmethod
    def to_bill_obj(cls, payment_plan, beneficiary, amount):
        bill = {}
        cls._build_subject(bill, beneficiary)
        cls._build_thirdparty(bill, payment_plan)
        cls._build_code(bill, beneficiary, beneficiary)
        cls._build_price(bill, amount)
        cls._build_terms(bill, payment_plan)
        cls._build_date_dates(bill, beneficiary)
        cls._build_currency(bill)
        cls._build_status(bill)
        return bill

    @classmethod
    def _build_subject(cls, bill, beneficiary):
        bill["subject_id"] = beneficiary.id
        bill['subject_type'] = ContentType.objects.get_for_model(beneficiary)

    @classmethod
    def _build_thirdparty(cls, bill, payment_plan):
        bill["thirdparty_id"] = payment_plan.benefit_plan.id
        bill['thirdparty_type'] = ContentType.objects.get_for_model(payment_plan.benefit_plan)

    @classmethod
    def _build_code(cls, bill, payment_plan, beneficiary):
        from core import datetime
        date = datetime.date.today()
        bill["code"] = f"{payment_plan.benefit_plan.code}-{date}: " \
                       f"{beneficiary.individual.first_name} {beneficiary.individual.last_name}"

    @classmethod
    def _build_price(cls, bill, amount):
        bill["amount_net"] = amount

    @classmethod
    def _build_date_dates(cls, bill, payment_plan):
        from core import datetime, datetimedelta
        bill["date_due"] = datetime.date.today() + datetimedelta(days=30)
        bill["date_bill"] = datetime.date.today()
        bill["date_valid_from"] = payment_plan.benefit_plan.date_valid_from
        bill["date_valid_to"] = payment_plan.benefit_plan.date_valid_to

    @classmethod
    def _build_currency(cls, bill):
        bill["currency_tp_code"] = InvoiceConfig.default_currency_code
        bill["currency_code"] = InvoiceConfig.default_currency_code

    @classmethod
    def _build_status(cls, bill):
        bill["status"] = Bill.Status.VALIDATED.value

    @classmethod
    def _build_terms(cls, bill, payment_plan):
        bill["terms"] = f'{payment_plan.benefit_plan.name}'
