from calcrule_social_protection.strategies import (
    BenefitPackageStrategyStorage
)
from calcrule_social_protection.config import CLASS_RULE_PARAM_VALIDATION, DESCRIPTION_CONTRIBUTION_VALUATION, FROM_TO
from core.abs_calculation_rule import AbsCalculationRule
from core.signals import *
from core import datetime


class SocialProtectionCalculationRule(AbsCalculationRule):
    version = 1
    uuid = "32d96b58-898a-460a-b357-5fd4b95cd87c"
    calculation_rule_name = "Calculation rule: social protection"
    description = DESCRIPTION_CONTRIBUTION_VALUATION
    impacted_class_parameter = CLASS_RULE_PARAM_VALIDATION
    date_valid_from = datetime.datetime(2000, 1, 1)
    date_valid_to = None
    status = "active"
    from_to = FROM_TO
    type = "social_protection"
    sub_type = "benefit_plan"
    CLASS_NAME_CHECK = ['PaymentPlan']

    signal_get_rule_name = Signal(providing_args=[])
    signal_get_rule_details = Signal(providing_args=[])
    signal_get_param = Signal(providing_args=[])
    signal_get_linked_class = Signal(providing_args=[])
    signal_calculate_event = Signal(providing_args=[])
    signal_convert_from_to = Signal(providing_args=[])

    @classmethod
    def ready(cls):
        now = datetime.datetime.now()
        condition_is_valid = (now >= cls.date_valid_from and now <= cls.date_valid_to) \
            if cls.date_valid_to else (now >= cls.date_valid_from and cls.date_valid_to is None)
        if condition_is_valid:
            if cls.status == "active":
                # register signals getParameter to getParameter signal and getLinkedClass ot getLinkedClass signal
                cls.signal_get_rule_name.connect(cls.get_rule_name, dispatch_uid="on_get_rule_name_signal")
                cls.signal_get_rule_details.connect(cls.get_rule_details, dispatch_uid="on_get_rule_details_signal")
                cls.signal_get_param.connect(cls.get_parameters, dispatch_uid="on_get_param_signal")
                cls.signal_get_linked_class.connect(cls.get_linked_class, dispatch_uid="on_get_linked_class_signal")
                cls.signal_calculate_event.connect(cls.run_calculation_rules, dispatch_uid="on_calculate_event_signal")
                cls.signal_convert_from_to.connect(cls.run_convert, dispatch_uid="on_convert_from_to")

    @classmethod
    def run_calculation_rules(cls, sender, payment_plan, user, context, **kwargs):
        return cls.calculate_if_active_for_object(payment_plan, **kwargs)

    @classmethod
    def calculate_if_active_for_object(cls, payment_plan, **kwargs):
        if cls.active_for_object(payment_plan):
            return cls.calculate(payment_plan, **kwargs)

    @classmethod
    def active_for_object(cls, payment_plan):
        return cls.check_calculation(payment_plan)

    @classmethod
    def get_linked_class(cls, sender, class_name, **kwargs):
        return ["Calculation"]

    @classmethod
    def get_parameters(cls, sender, class_name, instance, **kwargs):
        rule_details = cls.get_rule_details(sender=sender, class_name=class_name)
        if rule_details:
            if instance.__class__.__name__ in cls.CLASS_NAME_CHECK:
                if cls.check_calculation(payment_plan=instance):
                    return rule_details["parameters"] if "parameters" in rule_details else []
            elif instance.__class__.__name__ == 'ABCMeta' and cls.uuid == str(instance.uuid):
                return rule_details["parameters"] if "parameters" in rule_details else []

    @classmethod
    def run_convert(cls, payment_plan, **kwargs):
        return cls.convert(payment_plan=payment_plan, **kwargs)

    @classmethod
    def check_calculation(cls, payment_plan, **kwargs):
        return BenefitPackageStrategyStorage.choose_strategy(payment_plan).check_calculation(cls, payment_plan)

    @classmethod
    def calculate(cls, payment_plan, **kwargs):
        BenefitPackageStrategyStorage.choose_strategy(payment_plan).calculate(cls, payment_plan, **kwargs)

    @classmethod
    def convert(cls, payment_plan, **kwargs):
        BenefitPackageStrategyStorage.choose_strategy(payment_plan).convert(payment_plan, **kwargs)

    @classmethod
    def get_payment_cycle_parameters(cls, **kwargs):
        audit_user_id = kwargs.get('audit_user_id', None)
        start_date = kwargs.get('start_date', None)
        end_date = kwargs.get('end_date', None)
        payment_cycle = kwargs.get('payment_cycle', None)
        return audit_user_id, start_date, end_date, payment_cycle
