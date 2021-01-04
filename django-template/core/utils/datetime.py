from django.utils import timezone


def get_uts():
    return round(timezone.now().timestamp() * 1000)
