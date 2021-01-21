import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task
def notify_payment_system(order_id):
    from orders.services.order import OrderService
    order = OrderService.filter(pk=order_id).first()
    OrderService.notify_payment_system_done(order)


@app.task
def notify_logistics_system(order_id):
    from orders.services.order import OrderService
    order = OrderService.filter(pk=order_id).first()
    OrderService.notify_logistics_system_done(order)


@app.task
def send_email(order_id):
    from orders.services.order import OrderService
    order = OrderService.filter(pk=order_id).first()
    OrderService.send_email_done(order)
