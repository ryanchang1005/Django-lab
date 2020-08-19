from collections import namedtuple

from django.core.cache import cache

from users.models import TYPE_MY_USER, TYPE_APP_USER, MyUser, AppUser

UserCacheObject = namedtuple('UserCacheObject', ['id', 'sign_pub_key', 'uts'])


def set_user_cache_object(user_type, user_object, uts):
    k = f'{user_type}:{user_object.api_token}'
    v = [user_object.id, user_object.sign_pub_key, uts]
    cache.set(k, v)
    return UserCacheObject(*v)


def get_user_cache_object(user_type, token):
    k = f'{user_type}:{token}'
    v = cache.get(k)
    if v:
        # in cache
        return UserCacheObject(*v)
    else:
        # not in cache, query and set in cache
        if user_type == TYPE_MY_USER:
            try:
                user = MyUser.objects.get(api_token=token)
            except MyUser.DoesNotExist:
                return None
        elif user_type == TYPE_APP_USER:
            try:
                user = AppUser.objects.get(api_token=token)
            except AppUser.DoesNotExist:
                return None
        else:
            raise NotImplementedError

        return set_user_cache_object(user_type, user, 0)
