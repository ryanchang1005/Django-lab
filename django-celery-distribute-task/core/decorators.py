from functools import wraps

from core.schedule_lock import ScheduleLockService


def schedule_lock(name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 如有傳入node_list, name的後面需帶入node
            if 'node_list' in kwargs:
                node_str = ','.join([str(it) for it in kwargs['node_list']])
                final_name = f'{name}:{node_str}'  # name:1,2,3
            else:
                final_name = name  # name

            if ScheduleLockService.is_lock(final_name):
                print(f'{final_name} is locking')
                return None

            ScheduleLockService.lock(final_name)

            func(*args, **kwargs)

            ScheduleLockService.unlock(final_name)

        return wrapper

    return decorator
