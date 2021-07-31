from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from core.utils.datetime import get_datetime_display
from orders.models import Order
from orders.services.order import OrderService


@require_http_methods(['GET'])
def index(request):
    order_list = []

    qs = OrderService.filter()

    for it in qs:
        order_list.append({
            'pk': it.id,
            'create_type_display': it.get_create_type_display(),
            'create_time': get_datetime_display(it.create_time),
            'notify_payment_system_done_time': get_datetime_display(
                it.notify_payment_system_done_time) if it.notify_payment_system_done_time else '',
            'notify_logistics_system_done_time': get_datetime_display(
                it.notify_logistics_system_done_time) if it.notify_logistics_system_done_time else '',
            'send_email_done_time': get_datetime_display(it.send_email_done_time) if it.send_email_done_time else '',
            'done_duration': OrderService.get_done_duration(it),
        })

    return render(request, 'index.html', context={
        'order_list': order_list,

        # options
        'create_type_options': OrderService.get_create_type_options(),
    })


@require_http_methods(['POST'])
def create(request):
    create_type = request.POST.get('create_type')

    OrderService.create(
        create_type=create_type
    )

    return HttpResponseRedirect(reverse('index'))


@require_http_methods(['POST'])
def delete(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.delete()
    return HttpResponseRedirect(reverse('index'))
