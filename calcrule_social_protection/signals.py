import logging

from core.models import InteractiveUser, User
from core.service_signals import ServiceSignalBindType
from core.signals import bind_service_signal

from openIMIS.openimisapps import openimis_apps

from individual.models import IndividualDataSourceUpload
from social_protection.models import BenefitPlanDataUploadRecords, BenefitPlan
from social_protection.services import BenefitPlanService
from tasks_management.models import Task
from tasks_management.services import TaskService

logger = logging.getLogger(__name__)
imis_modules = openimis_apps()


def bind_service_signals():

    def on_task_complete_benefit_plan_update(**kwargs):
        try:
            result = kwargs.get('result', None)
            if result \
                    and result['success'] \
                    and result['data']['task']['business_event'] == 'benefit_plan_update' \
                    and result['data']['task']['status'] == Task.Status.COMPLETED:
                user = User.objects.get(id=result['data']['user']['id'])
                BenefitPlanService(user).update(result['data']['task']['data'])
        except Exception as e:
            logger.error("Error while executing on_task_complete_benefit_plan_update", exc_info=e)

    def on_task_resolve_benefit_plan_update(**kwargs):
        def resolve_task_all(_task, _user):
            if 'FAILED' in _task.business_status.values():
                TaskService(_user).complete_task({"id": _task.id, 'failed': True})
            if sum(map('APPROVED'.__eq__, _task.business_status.values())) == _task.task_group.taskexecutor_set.count():
                TaskService(_user).complete_task({"id": _task.id})

        def resolve_task_any(_task, _user):
            if 'FAILED' in _task.business_status.values():
                TaskService(_user).complete_task({"id": _task.id, 'failed': True})
            if 'APPROVED' in _task.business_status.values():
                TaskService(_user).complete_task({"id": _task.id})

        def resolve_task_n(_task, _user):
            # TODO for now hardcoded to any, to be updated
            resolve_task_any(_task, _user)

        try:
            result = kwargs.get('result', None)
            if result and result['success'] \
                    and result['data']['task']['business_event'] == 'benefit_plan_update' \
                    and result['data']['task']['status'] == Task.Status.ACCEPTED:
                data = kwargs.get("result").get("data")
                task = Task.objects.select_related('task_group').prefetch_related('task_group__taskexecutor_set').get(
                    id=data["task"]["id"])
                user = User.objects.get(id=data["user"]["id"])

                if not task.task_group:
                    logger.error("Resolving task not assigned to TaskGroup")
                    return ['Task not assigned to TaskGroup']

                resolvers = {
                    'ALL': resolve_task_all,
                    'ANY': resolve_task_any,
                    'N': resolve_task_n,
                }

                if task.task_group.completion_policy not in resolvers:
                    logger.error("Resolving task with unknown completion_policy: %s", task.task_group.completion_policy)
                    return ['Unknown completion_policy: %s' % task.task_group.completion_policy]

                resolvers[task.task_group.completion_policy](task, user)
        except Exception as e:
            logger.error("Error while executing on_task_resolve_benefit_plan_update", exc_info=e)
            return [str(e)]

    bind_service_signal(
        'task_service.complete_task',
        on_task_complete_benefit_plan_update,
        bind_type=ServiceSignalBindType.AFTER
    )
    bind_service_signal(
        'task_service.resolve_task',
        on_task_resolve_benefit_plan_update,
        bind_type=ServiceSignalBindType.AFTER
    )
