try:
    from modeltranslation.translator import TranslationOptions, register
except ModuleNotFoundError:
    from django.contrib.admin import register, ModelAdmin as TranslationOptions


from .models import (
    AdministrativeAreaLevel1,
    AdministrativeAreaLevel2,
    AdministrativeAreaLevel3,
    AdministrativeAreaLevel4,
    AdministrativeAreaLevel5,
    Locality,
    Neighborhood,
    Place,
    Route,
    SubLocalityLevel1,
    SubLocalityLevel2,
    SubLocalityLevel3,
    SubLocalityLevel4,
    SubLocalityLevel5,
)


@register(Place)
class PlaceTranslationOptions(TranslationOptions):
    fields = ("formatted_address", "street_number", "floor", "room")


class AddressComponentTranslationOptions(TranslationOptions):
    fields = ("long_name", "short_name")


@register(AdministrativeAreaLevel1)
class AdministrativeAreaLevel1TranslationOptions(
    AddressComponentTranslationOptions
):
    pass


@register(AdministrativeAreaLevel2)
class AdministrativeAreaLevel2TranslationOptions(
    AddressComponentTranslationOptions
):
    pass


@register(AdministrativeAreaLevel3)
class AdministrativeAreaLevel3TranslationOptions(
    AddressComponentTranslationOptions
):
    pass


@register(AdministrativeAreaLevel4)
class AdministrativeAreaLevel4TranslationOptions(
    AddressComponentTranslationOptions
):
    pass


@register(AdministrativeAreaLevel5)
class AdministrativeAreaLevel5TranslationOptions(
    AddressComponentTranslationOptions
):
    pass


@register(Locality)
class LocalityTranslationOptions(AddressComponentTranslationOptions):
    pass


@register(SubLocalityLevel1)
class SubLocalityLevel1TranslationOptions(AddressComponentTranslationOptions):
    pass


@register(SubLocalityLevel2)
class SubLocalityLevel2TranslationOptions(AddressComponentTranslationOptions):
    pass


@register(SubLocalityLevel3)
class SubLocalityLevel3TranslationOptions(AddressComponentTranslationOptions):
    pass


@register(SubLocalityLevel4)
class SubLocalityLevel4TranslationOptions(AddressComponentTranslationOptions):
    pass


@register(SubLocalityLevel5)
class SubLocalityLevel5TranslationOptions(AddressComponentTranslationOptions):
    pass


@register(Neighborhood)
class NeighborhoodTranslationOptions(AddressComponentTranslationOptions):
    pass


@register(Route)
class RouteTranslationOptions(AddressComponentTranslationOptions):
    pass
