# Django-Celery-RabbitMQ

## Containers
* app
* celery-worker
* rabbitmq

## Simulate order creation
1. Create order(0s)
1. Notify payment system(3s)
2. Notify logistics system(3s)
3. Send email(3s)


## YA
```
sync
total time = 0 + 3 + 3 + 3 = 9
request > Create order(0s) > Notify payment system(3s) > Notify logistics system(3s) > Send email(3s)


async
total time = 0 + 3 = 3
                             - Notify payment system(3s)(async)
                            /
request > Create order(0s) --- Notify logistics system(3s)(async)
                            \
                             - Send email(3s)(async)
```

## Model
```
class Order:
    create_type(str)(SYNC | ASYNC_WITH_MQ)
    create_time(DateTime)
    notify_payment_system_done_time(DateTime)
    notify_logistics_system_done_time(DateTime)
    send_email_done_time(DateTime)
```
1, SYNC, 8s
2, ASYNC_WITH_MQ, 4s