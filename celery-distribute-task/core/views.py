from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from core.models import Config
from tasks.models import Task
from tasks.services import TaskService


def index(request):
    task_list = []
    qs = Task.objects.order_by('-id')[:100]
    for it in qs:
        task_list.append({
            'id': it.id,
            'done_time': str(it.done_time),
            'node': it.node,
        })

    config = Config.objects.all().first()
    distribute_task_count = 0
    if config:
        distribute_task_count=config.distribute_task_count
    return render(request, 'index.html', context={
        'task_list': task_list,
        'distribute_task_count': distribute_task_count,
    })


def create(request):
    count = request.POST.get('count')
    TaskService.batch_create(int(count))
    return HttpResponseRedirect(reverse('index'))


def update_config(request):
    distribute_task_count = request.POST.get('distribute_task_count')

    # get_or_create
    config = Config.objects.all().first()
    if config is None:
        config = Config.objects.create()

    config.distribute_task_count = int(distribute_task_count)
    config.save(update_fields=['distribute_task_count'])
    return HttpResponseRedirect(reverse('index'))
