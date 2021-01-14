import logging
import random
import secrets

from django.http import JsonResponse

logger = logging.getLogger(__name__)


def get_random_message():
    return secrets.token_hex()


def info(request):
    for i in range(random.randint(5, 10)):
        logger.info(f'info({get_random_message()})')

    return JsonResponse({'type': 'info'})


def error(request):
    for i in range(random.randint(5, 10)):
        logger.info(f'error({get_random_message()})')

    return JsonResponse({'type': 'error'})
