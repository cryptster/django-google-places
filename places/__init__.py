from django.conf import settings

import redis


pool = redis.ConnectionPool.from_url(f'{settings.REDIS_DSN}/4')
redis_conn = redis.Redis(connection_pool=pool)
