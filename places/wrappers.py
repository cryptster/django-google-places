import pickle

from django.conf import settings
from django.core.cache import caches


class CacheableWrapper:
    def __init__(self, client, cache_name='default'):
        """
        :param client : instance googlemaps Client.
        :param cache_name : keys for caches.
        """
        self._client = client
        self.cache = caches[cache_name]

    def __getattr__(self, name):
        attr = getattr(self._client, name)
        is_callable = callable(attr)

        def handler(*args, **kwargs):
            cache_key = f"{name}::{args}::{kwargs}"
            cached_result = self.cache.get(cache_key)

            if cached_result:
                result = pickle.loads(cached_result)
            else:
                result = attr
                if is_callable:
                    result = result(*args, **kwargs)
                    pickled_object = pickle.dumps(result)
                    self.cache.set(cache_key, pickled_object, settings.CACHING_TIME)

            return result

        return handler if is_callable else handler()
