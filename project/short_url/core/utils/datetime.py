import pytz

from django.utils import timezone


def to_iso8601_utc_string(datetime_obj):
    utc_datetime = datetime_obj.astimezone(pytz.utc)
    return utc_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')


def get_locale_str_by_utc_datetime_obj(utc_datetime_obj):
    locale_datetime_obj = utc_datetime_obj.astimezone(timezone.get_current_timezone())
    return locale_datetime_obj.strftime('%Y/%m/%d %H:%M:%S')


def get_now_datetime_obj():
    return timezone.now()
