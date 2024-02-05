import json
import logging

from calcrule_social_protection.apps import CalcruleSocialProtectionConfig
from core.models import User
from core.service_signals import ServiceSignalBindType
from core.signals import bind_service_signal

from openIMIS.openimisapps import openimis_apps

from calcrule_social_protection.strategies import BaseBenefitPackageStrategy
from invoice.models import Bill
from tasks_management.models import Task

logger = logging.getLogger(__name__)
imis_modules = openimis_apps()


def bind_service_signals():

    def on_task_complete_calculate(**kwargs):
        def create_bill(results, convert_benefit, payroll_id, bill_status):
            user = User.objects.get(id=result['data']['user']['id'])
            results['user'] = user
            BaseBenefitPackageStrategy.create_and_save_business_entities(
                results,
                convert_benefit,
                payroll_id,
                user,
                bill_status
            )

        try:
            result = kwargs.get('result', None)
            task = result['data']['task']
            if result \
                    and result['success'] \
                    and task['business_event'] == CalcruleSocialProtectionConfig.calculate_business_event:
                convert_results = task['data']
                convert_results = convert_results.replace("'", '"')
                convert_results = json.loads(convert_results)
                task_status = task['status']
                convert_benefit = convert_results.pop("benefit", None)
                payroll_id = convert_results.pop("payroll_id", None)
                if task_status == Task.Status.COMPLETED:
                    create_bill(convert_results, convert_benefit, payroll_id, Bill.Status.VALIDATED)
                if task_status == Task.Status.FAILED:
                    create_bill(convert_results, convert_benefit, payroll_id, Bill.Status.CANCELLED)
                else:
                    pass
        except Exception as e:
            logger.error("Error while executing on_task_complete_calculate", exc_info=e)

    bind_service_signal(
        'task_service.complete_task',
        on_task_complete_calculate,
        bind_type=ServiceSignalBindType.AFTER
    )
