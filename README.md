# Django google places

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/tlsfuzzer/python-ecdsa.svg?logo=lgtm&logoWidth=18)]
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat)


Django Google Places is a Django plug-in, that helps cache responses from GoogleMaps.  
This feature helps to reduce the number of requests for third-party resources, which will speed up the performance of your application. 

## Features

Django plug-in for address auto-fill in Google Places. 

## Dependencies

- Python 3.7 or later.
- Django 2.2 or later.
- googlemaps 4.2.0.

## Installation

This library is available in PyPI. It is advisable to use `pip` during installation: 

```
pip install django-google-places
```

## Testing

To run a complete set of tests, do the following: 

    make test-all

## Usage

- Add ``'places'`` entries to Django’s ``INSTALLED_APPS`` settings.

- Supports packages``modeltranslation`` and ``django_countries`` (optional).

- For each Google Maps web service request, API key or client identifier is required.  
API keys can be created on 'APIs & Services' page at  https://console.cloud.google.com/apis/credentials .
More information on how to get started with Google Maps platform, and further information on creation/limitations of API key, see section Getting started with Google Maps Platform at https://developers.google.com/maps/gmp-get-started.

- Add your Google Maps API key to your ``settings.ru`` as ``GOOGLE_MAPS_API_KEY`` and caching time as  ``CACHING_TIME``. Also addread.me ``GOOGLE_PLACES_WRAPPER_CACHE_NAME`` key for caching. By default, 'default' is used. Other settings are optional – see Google Maps instructions. 
```python
        GOOGLE_PLACES_API_KEY="AIzaDummyKey",
        CACHING_TIME=60 * 60 * 24,
        MODELTRANSLATION_LANGUAGES=("en", "ru", "es"),
        TIME_ZONE="UTC",
        USE_TZ=True,
        USE_I18N=True,
```

- Run migrations to upload models to your database:

```
python manage.py migrate places
```

- Google Maps responses can be saved in model ``Place`` whose manager is written for Google Maps response for "types" key, and fills the following related models:

```
AdministrativeAreaLevel1,
AdministrativeAreaLevel2,
AdministrativeAreaLevel3,
AdministrativeAreaLevel4,
AdministrativeAreaLevel5,
Locality,
SubLocalityLevel1,
SubLocalityLevel2,
SubLocalityLevel3,
SubLocalityLevel4,
SubLocalityLevel5,
Neighborhood,
Route
```

- ``Django-google-places`` supports all methods  ``google-maps-services-python`` https://github.com/googlemaps/google-maps-services-python Example of using  django-google-places  caching decorator:

```python
from datetime import datetime
from places.clients import cacheable_gmaps

# Geocoding an address
geocode_result = cacheable_gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
# Look up an address with reverse geocoding
reverse_geocode_result = cacheable_gmaps.reverse_geocode((40.714224, -73.961452))
# Request directions via public transit
now = datetime.now()
directions_result = cacheable_gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)
```


