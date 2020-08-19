from datetime import datetime

from django.core.cache import cache


class ScheduleLockService:

    @staticmethod
    def get_key(name):
        return f'schedule_lock:{name}'

    @staticmethod
    def lock(name):
        key = ScheduleLockService.get_key(name)
        # 排程名稱:執行時間

        cache.set(key, datetime.now(), 10 * 60)  # 鎖最多10分鐘

    @staticmethod
    def unlock(name):
        key = ScheduleLockService.get_key(name)
        cache.delete(key)

    @staticmethod
    def is_lock(name):
        key = ScheduleLockService.get_key(name)
        for k in cache.keys(f'*{key}*'):
            if cache.get(k) is not None:
                return True
        return False

    @staticmethod
    def get_lock_datetime(name):
        key = ScheduleLockService.get_key(name)
        ret = []
        for k in cache.keys(f'*{key}*'):
            if cache.get(k) is not None:
                ret.append(cache.get(k))
        return ret
