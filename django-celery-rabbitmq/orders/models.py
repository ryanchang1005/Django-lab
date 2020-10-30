from django.db import models


class Order(models.Model):
    CREATE_TYPE_SYNC = 'SYNC'
    CREATE_TYPE_ASYNC = 'ASYNC'

    CREATE_TYPE_CHOICE = (
        (CREATE_TYPE_SYNC, 'sync'),
        (CREATE_TYPE_ASYNC, 'async'),
    )

    create_type = models.CharField(
        max_length=10,
        choices=CREATE_TYPE_CHOICE,
    )

    create_time = models.DateTimeField(auto_now_add=True)

    notify_payment_system_done_time = models.DateTimeField(null=True)

    notify_logistics_system_done_time = models.DateTimeField(null=True)

    send_email_done_time = models.DateTimeField(null=True)
