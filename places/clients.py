from django.conf import settings
from googlemaps import Client

from places.wrappers import CacheableWrapper

cacheable_gmaps = CacheableWrapper(Client(key=settings.GOOGLE_PLACES_API_KEY))
