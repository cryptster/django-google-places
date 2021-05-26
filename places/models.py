"""
Google places Address Types and Address Component Types
https://developers.google.com/maps/documentation/geocoding/intro#Types
"""
from typing import Type, TypeVar

from django.conf import settings
from django.db import models

from places.clients import cacheable_gmaps

try:
    from django_countries.fields import CountryField
except ModuleNotFoundError:
    from django.db.models import TextField as CountryField

DjModel = TypeVar("DjModel", bound=models.Model)


class AddressComponent(models.Model):
    long_name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50)

    class Meta:
        abstract = True


class AdministrativeAreaLevel1(AddressComponent):
    pass


class AdministrativeAreaLevel2(AddressComponent):
    pass


class AdministrativeAreaLevel3(AddressComponent):
    pass


class AdministrativeAreaLevel4(AddressComponent):
    pass


class AdministrativeAreaLevel5(AddressComponent):
    pass


class Locality(AddressComponent):
    pass


class SubLocalityLevel1(AddressComponent):
    pass


class SubLocalityLevel2(AddressComponent):
    pass


class SubLocalityLevel3(AddressComponent):
    pass


class SubLocalityLevel4(AddressComponent):
    pass


class SubLocalityLevel5(AddressComponent):
    pass


class Neighborhood(AddressComponent):
    pass


class Route(AddressComponent):
    pass


class PlaceManager(models.Manager):
    def get_details(self, address: str):
        candidates = cacheable_gmaps.find_place(
            input=address,
            input_type="textquery",
        )

        if candidates["status"] != "OK":
            return None

        place_id = candidates["candidates"][0]["place_id"]

        try:
            return self.model.objects.get(place_id=place_id)
        except self.model.DoesNotExist:
            pass

        details = {}
        for lang in settings.MODELTRANSLATION_LANGUAGES:
            details[lang] = cacheable_gmaps.place(
                place_id,
                language=lang,
            )["result"]

        defaults = {}
        # formatted_address
        defaults.update(self.get_formatted_address(details))
        # country
        try:
            defaults["country"] = self.get_country_code(details)
        except StopIteration:  # For example: Малые Антильские острова
            return None
        # administrative_area_level
        defaults["administrative_area_level_1"] = self.get_component_object(
            AdministrativeAreaLevel1, "administrative_area_level_1", details
        )
        defaults["administrative_area_level_2"] = self.get_component_object(
            AdministrativeAreaLevel2, "administrative_area_level_2", details
        )
        defaults["administrative_area_level_3"] = self.get_component_object(
            AdministrativeAreaLevel3, "administrative_area_level_3", details
        )
        defaults["administrative_area_level_4"] = self.get_component_object(
            AdministrativeAreaLevel4, "administrative_area_level_4", details
        )
        defaults["administrative_area_level_5"] = self.get_component_object(
            AdministrativeAreaLevel1, "administrative_area_level_5", details
        )
        # locality
        defaults["locality"] = self.get_component_object(
            Locality,
            "locality",
            details,
        )
        # sublocality_level
        defaults["sublocality_level_1"] = self.get_component_object(
            SubLocalityLevel1, "sublocality_level_1", details
        )
        defaults["sublocality_level_2"] = self.get_component_object(
            SubLocalityLevel2, "sublocality_level_2", details
        )
        defaults["sublocality_level_3"] = self.get_component_object(
            SubLocalityLevel3, "sublocality_level_3", details
        )
        defaults["sublocality_level_4"] = self.get_component_object(
            SubLocalityLevel4, "sublocality_level_4", details
        )
        defaults["sublocality_level_5"] = self.get_component_object(
            SubLocalityLevel5, "sublocality_level_5", details
        )
        # neighborhood
        defaults["neighborhood"] = self.get_component_object(
            Neighborhood, "neighborhood", details
        )
        # route
        defaults["route"] = self.get_component_object(Route, "route", details)
        # street_number
        defaults.update(self.get_street_number(details))
        # floor
        defaults.update(self.get_floor(details))
        # room
        defaults.update(self.get_room(details))
        # postal_code
        defaults["postal_code"] = self.get_postal_code(details)
        # lat and lng
        defaults.update(self.get_lat_lng(details))

        return self.model.objects.create(place_id=place_id, **defaults)

    @staticmethod
    def get_component_object(
        model: Type[DjModel], key: str, data: dict
    ) -> models.Model or None:
        kwargs = {}

        for lang in settings.MODELTRANSLATION_LANGUAGES:
            for item in data[lang]["address_components"]:
                if key in item["types"]:
                    kwargs[f"long_name_{lang}"] = item["long_name"]
                    kwargs[f"short_name_{lang}"] = item["short_name"]

        if kwargs:
            p, _ = model.objects.get_or_create(**kwargs)
            return p
        return None

    @staticmethod
    def get_formatted_address(details: dict) -> dict:
        defaults = {}
        for lang in settings.MODELTRANSLATION_LANGUAGES:
            defaults[f"formatted_address_{lang}"] = details[lang][
                "formatted_address"
            ]
        return defaults

    @staticmethod
    def get_country_code(details: dict) -> str:
        return next(
            filter(
                lambda x: x if "country" in x["types"] else None,
                details["en"]["address_components"],
            )
        )["short_name"]

    @staticmethod
    def get_street_number(details: dict) -> dict:
        defaults = {}
        for lang in settings.MODELTRANSLATION_LANGUAGES:
            numbers = list(
                filter(
                    lambda x: x if "street_number" in x["types"] else None,
                    details[lang]["address_components"],
                )
            )
            if numbers:
                defaults[f"street_number_{lang}"] = numbers[0]["long_name"]
        return defaults

    @staticmethod
    def get_floor(details: dict) -> dict:
        defaults = {}
        for lang in settings.MODELTRANSLATION_LANGUAGES:
            numbers = list(
                filter(
                    lambda x: x if "floor" in x["types"] else None,
                    details[lang]["address_components"],
                )
            )
            if numbers:
                defaults[f"floor_{lang}"] = numbers[0]["long_name"]
        return defaults

    @staticmethod
    def get_room(details: dict) -> dict:
        defaults = {}
        for lang in settings.MODELTRANSLATION_LANGUAGES:
            numbers = list(
                filter(
                    lambda x: x if "room" in x["types"] else None,
                    details[lang]["address_components"],
                )
            )
            if numbers:
                defaults[f"room_{lang}"] = numbers[0]["long_name"]
        return defaults

    @staticmethod
    def get_postal_code(details: dict) -> str:
        postal = list(
            filter(
                lambda x: x if "postal_code" in x["types"] else None,
                details["en"]["address_components"],
            )
        )
        if postal:
            return postal[0]["long_name"]
        return ""

    @staticmethod
    def get_lat_lng(details: dict) -> dict:
        defaults = {}
        if "geometry" in details["en"]:
            if "location" in details["en"]["geometry"]:
                defaults["latitude"] = details["en"]["geometry"]["location"][
                    "lat"
                ]
                defaults["longitude"] = details["en"]["geometry"]["location"][
                    "lng"
                ]
        return defaults


class Place(models.Model):
    place_id = models.CharField(max_length=250, unique=True)
    formatted_address = models.CharField(max_length=250)
    country = CountryField()
    administrative_area_level_1 = models.ForeignKey(
        AdministrativeAreaLevel1,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    administrative_area_level_2 = models.ForeignKey(
        AdministrativeAreaLevel2,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    administrative_area_level_3 = models.ForeignKey(
        AdministrativeAreaLevel3,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    administrative_area_level_4 = models.ForeignKey(
        AdministrativeAreaLevel4,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    administrative_area_level_5 = models.ForeignKey(
        AdministrativeAreaLevel5,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    locality = models.ForeignKey(
        Locality, blank=True, null=True, on_delete=models.CASCADE
    )
    sublocality_level_1 = models.ForeignKey(
        SubLocalityLevel1, blank=True, null=True, on_delete=models.CASCADE
    )
    sublocality_level_2 = models.ForeignKey(
        SubLocalityLevel2, blank=True, null=True, on_delete=models.CASCADE
    )
    sublocality_level_3 = models.ForeignKey(
        SubLocalityLevel3, blank=True, null=True, on_delete=models.CASCADE
    )
    sublocality_level_4 = models.ForeignKey(
        SubLocalityLevel4, blank=True, null=True, on_delete=models.CASCADE
    )
    sublocality_level_5 = models.ForeignKey(
        SubLocalityLevel5, blank=True, null=True, on_delete=models.CASCADE
    )
    neighborhood = models.ForeignKey(
        Neighborhood, blank=True, null=True, on_delete=models.CASCADE
    )
    route = models.ForeignKey(
        Route, blank=True, null=True, on_delete=models.CASCADE
    )
    street_number = models.CharField(max_length=10, blank=True)
    floor = models.CharField(max_length=10, blank=True)
    room = models.CharField(max_length=10, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)

    objects = PlaceManager()

    def __str__(self):
        return self.formatted_address
