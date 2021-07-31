from django.core.cache import cache

from shorturl.models import ShortURL


class ShortURLService:

    @staticmethod
    def get_url_with_cache(code):
        key = f'short_url.{code}.url'
        val = cache.get(key)
        if val:
            return val
        else:
            obj = ShortURL.objects.filter(code=code).first()

            # 找不到此短連結, 把None設為cache
            if not obj:
                val = {'url': None}
                cache.set(key, val, 1 * 60)
                return val

            # 將url, 設為cache
            val = {'url': obj.url}
            cache.set(key, val, 1 * 60)
            return val
