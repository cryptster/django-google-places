import pickle

from django.conf import settings
from django.core.cache import cache


class CacheableWrapper:
    def __init__(self, client):
        self._client = client

    def __getattr__(self, name):
        attr = getattr(self._client, name)
        is_callable = callable(attr)


        def handler(*args, **kwargs):
            cache_key = f'{name}::{args}::{kwargs}'
            cached_result = cache.get(cache_key)

            if cached_result:
                result = pickle.loads(cached_result)
            else:
                result = attr
                if is_callable:
                    result = result(*args, **kwargs)
                    pickled_object = pickle.dumps(result)
                    cache.set(cache_key, pickled_object, settings.CACHING_TIME)

            return result

        return handler if is_callable else handler()
