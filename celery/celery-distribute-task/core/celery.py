import os
from datetime import timedelta

from celery import Celery
from django.conf import settings

# 設置環境變量 DJANGO_SETTINGS_MODULE

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 創建實例
app = Celery('core')
app.config_from_object('django.conf:settings')

# 查找在 INSTALLED_APPS 設置的異步任務
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# 排程任務
app.conf.beat_schedule = {
    # 訂單相關
    'task_distributor': {
        'task': 'core.celery.task_distributor',
        'schedule': timedelta(seconds=30),
    }
}


@app.task(bind=True)
def task_distributor(self):
    from core.models import Config
    from tasks.models import Task
    from core.utils import MAX_NODE, NODES

    config = Config.objects.all().first()
    if config:
        count = Task.objects.filter(done_time__isnull=True).count()
        if count == 0:
            print('count == 0')
            return None

        # 複製nodes
        nodes = NODES.copy()

        # 拆成N個節點
        N = config.distribute_task_count

        # 1個節點一次執行幾個任務
        task_count_per_node = int(MAX_NODE / N)

        for i in range(N):
            if i == N - 1:
                # 最後一圈(直接把剩下的跑完)
                execute_task.delay(nodes)
            else:
                # 取出前task_count_per_node個任務執行並刪除拿走的任務node
                execute_task.delay(nodes[0:task_count_per_node])
                del nodes[0:task_count_per_node]


@app.task
def execute_task(node_list):
    from core.schedule import ScheduleService
    ScheduleService.execute_task(node_list=node_list)
