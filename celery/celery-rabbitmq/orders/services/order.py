from time import sleep

from core.celery import notify_payment_system, notify_logistics_system, send_email
from core.utils.datetime import get_now_datetime_obj
from orders.models import Order


class OrderService:

    @staticmethod
    def filter(pk=None):
        qs = Order.objects.all()

        if pk:
            qs = qs.filter(id=pk)

        return qs

    @staticmethod
    def create(create_type):
        order = Order()
        order.create_type = create_type
        order.save()

        if create_type == Order.CREATE_TYPE_SYNC:
            OrderService.notify_payment_system_done(order)
            OrderService.notify_logistics_system_done(order)
            OrderService.send_email_done(order)
        elif create_type == Order.CREATE_TYPE_ASYNC:
            notify_payment_system.delay(order.id)
            notify_logistics_system.delay(order.id)
            send_email.delay(order.id)

        return order

    @staticmethod
    def notify_payment_system_done(order):
        sleep(3)

        order.notify_payment_system_done_time = get_now_datetime_obj()
        order.save(update_fields=['notify_payment_system_done_time'])

    @staticmethod
    def notify_logistics_system_done(order):
        sleep(3)

        order.notify_logistics_system_done_time = get_now_datetime_obj()
        order.save(update_fields=['notify_logistics_system_done_time'])

    @staticmethod
    def send_email_done(order):
        sleep(3)

        order.send_email_done_time = get_now_datetime_obj()
        order.save(update_fields=['send_email_done_time'])

    @staticmethod
    def get_create_type_options():
        options = []
        for k, v in Order.CREATE_TYPE_CHOICE:
            options.append({
                'k': k,
                'v': v,
            })
        return options

    @staticmethod
    def get_done_duration(order):
        all_time = [order.create_time,
                    order.notify_payment_system_done_time,
                    order.notify_logistics_system_done_time,
                    order.send_email_done_time]

        if None in all_time:
            return '-'

        return (max(all_time) - min(all_time)).total_seconds()
