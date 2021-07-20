import time
from time import sleep

from django.http import JsonResponse
from rest_framework import status

from core.thread_executor import DjangoConnectionThreadPoolExecutor
from users.models import User


def request_with_for_loop(request):
    """
    以一般迴圈SELECT 10次, 分別以settings中CONN_MAX_AGE, 0 和 60測試
    """
    start = time.time()
    name_list = []
    for pk in range(1, 6):
        u = User.objects.get(id=pk)
        sleep(1)
        name_list.append(u.name)
    return JsonResponse(
        status=status.HTTP_200_OK,
        data={
            'message': 'OK',
            'time': time.time() - start,
            'data': name_list
        }
    )


def request_with_thread_pool_executor(request):
    start = time.time()

    def _get_user_name(pk):
        u = User.objects.get(id=pk)
        sleep(1)
        print(f'{pk} end')
        return u.name

    results = None
    with DjangoConnectionThreadPoolExecutor() as executor:
        results = executor.map(_get_user_name, [pk % 100 for pk in range(5000)])
        print(results)
    return JsonResponse(
        status=status.HTTP_200_OK,
        data={
            'message': 'OK',
            'time': time.time() - start,
            'data': results,
        }
    )


"""
使用底下SQL監控連線數
SELECT pid,
       usename,
       now() - backend_start AS duration,
       wait_event,
       state,
       query
FROM pg_stat_activity;
"""
