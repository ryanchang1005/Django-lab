from django.utils import timezone


def get_now_datetime_obj():
    return timezone.now()


def get_datetime_display(datetime_obj):
    return datetime_obj.strftime('%Y/%m/%d %H:%M:%S')
