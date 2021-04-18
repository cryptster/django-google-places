import os

import django
from django.conf import settings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "places"))


def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            }
        },
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS=(
            "modeltranslation",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "places",
            "django_countries",
        ),
        GOOGLE_PLACES_API_KEY="AIzaDummyKey",
        CACHING_TIME=60 * 60 * 24,
        MODELTRANSLATION_LANGUAGES=("en", "ru", "es"),
        TIME_ZONE="UTC",
        USE_TZ=True,
        USE_I18N=True,
    )

    django.setup()
