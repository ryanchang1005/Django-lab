import time
from datetime import datetime

from core.decorators import schedule_lock
from tasks.models import Task


class ScheduleService:

    @staticmethod
    @schedule_lock(name='ScheduleService.execute_task')
    def execute_task(node_list):
        qs = Task.objects.filter(done_time__isnull=True,
                                 node__in=node_list)

        if qs.count() == 0:
            return None

        for it in qs:
            it.done_time = datetime.now()
            it.save(update_fields=['done_time'])
            print(f'id={it.id}')
            time.sleep(1)
