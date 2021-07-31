import time

from django.core.cache import cache


class RateLimitService:
    RATE_LIMIT_COUNT_PER_SECOND = 5

    @staticmethod
    def touch_and_return_is_pass(key):
        """
        限制每秒 RATE_LIMIT_COUNT_PER_SECOND 次, Redis中key, value, TTL的變化
        Key的組成 = 前綴:Key:目前秒數
        key                     value       TTL
        rate_limit:xxx:0        1           1
        rate_limit:xxx:0        2           0.8
        rate_limit:xxx:0        3           0.7
        rate_limit:xxx:0        4           0.6
        rate_limit:xxx:0        5           0.2
        rate_limit:xxx:1        1           1
        """
        now_second = int(time.time() % 10)
        key = f'rate_limit:{key}:{now_second}'  # prefix:key:now_second
        value = cache.get(key)

        if value is not None:
            # cache is set
            if value >= RateLimitService.RATE_LIMIT_COUNT_PER_SECOND:
                # exceed rate limit
                return False
            else:
                # not exceed, increase count
                cache.incr(key)
        else:
            # cache not set, touch and set expire 1 seconds
            cache.set(key, 1, 1)
        return True
