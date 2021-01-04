import pytz
from django.utils import timezone


def get_uts():
    return round(timezone.now().timestamp() * 1000)


def to_iso8601_utc_string(datetime_obj):
    utc_datetime = datetime_obj.astimezone(pytz.utc)
    return utc_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
