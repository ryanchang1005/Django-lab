from django.utils import timezone


def get_now_datetime_obj():
    return timezone.now()


def get_datetime_format_iso8601(datetime_obj=get_now_datetime_obj()):
    return datetime_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
