import pytz

from django.utils import timezone
from datetime import datetime, timedelta


def get_uts():
    return round(timezone.now().timestamp() * 1000)


def get_uts_by_sec():
    return round(timezone.now().timestamp())


def get_locale_datetime_str_by_uts(uts):
    return datetime.fromtimestamp(uts).strftime('%Y/%m/%d %H:%M:%S')


def to_iso8601_utc_string(datetime_obj):
    utc_datetime = datetime_obj.astimezone(pytz.utc)
    return utc_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')


def iso8601_string_to_datetime_obj(value):
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')


def to_ymd_utc_string(datetime_obj):
    utc_datetime = datetime_obj.astimezone(pytz.utc)
    return utc_datetime.strftime('%Y-%m-%d')


def get_locale_str_by_utc_datetime_obj(utc_datetime_obj):
    locale_datetime_obj = utc_datetime_obj.astimezone(timezone.get_current_timezone())
    return locale_datetime_obj.strftime('%Y/%m/%d %H:%M:%S')


def get_locale_datetime_obj_by_date_str(date_str):
    # ex:2020-01-01
    return datetime.strptime(date_str, '%Y-%m-%d')


def get_now_datetime_obj():
    return timezone.now()


def utc_obj_to_locale_obj(utc_obj):
    return utc_obj.astimezone(timezone.get_current_timezone())


def get_utc_datetime_by_today_localtime_midnight():
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).astimezone(pytz.utc)


def locale_obj_to_utc_obj(locale_obj):
    return locale_obj.astimezone(pytz.utc)


def is_valid_date(text):
    if text is None:
        return False
    try:
        obj = datetime.strptime(text, '%Y-%m-%d')
        if not 1900 <= obj.year <= 3000 or \
                not 1 <= obj.month <= 12 or \
                not 1 <= obj.day <= 31:
            return False
        return True
    except ValueError:
        return False


def get_index_default_from_to_datetime_obj(from_date, to_date):
    """
    預設頁面起訖時間值
    """
    if not is_valid_date(from_date) or not is_valid_date(to_date):
        from_utc_obj = get_utc_datetime_by_today_localtime_midnight() - timedelta(days=30)
        to_utc_obj = from_utc_obj + timedelta(days=31, microseconds=-1)
    else:
        from_utc_obj = locale_obj_to_utc_obj(get_locale_datetime_obj_by_date_str(from_date))
        to_utc_obj = locale_obj_to_utc_obj(get_locale_datetime_obj_by_date_str(to_date))
        to_utc_obj = to_utc_obj + timedelta(days=1, microseconds=-1)  # 要包含今天一整天

    return from_utc_obj, to_utc_obj
