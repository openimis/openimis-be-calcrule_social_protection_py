class BenefitPackageStrategyInterface:

    TYPE = None
    BENEFICIARY_OBJECT = None
    BENEFICIARY_TYPE = None

    @classmethod
    def get_parameters(cls, sender, class_name, instance, **kwargs):
        pass

    @classmethod
    def check_calculation(cls, payment_plan, **kwargs):
        pass

    @classmethod
    def calculate(cls, payment_plan, beneficiary_object, beneficiary_type, **kwargs):
        pass

    @classmethod
    def convert(cls, payment_plan, **kwargs):
        pass
