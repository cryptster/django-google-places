from unittest.mock import call, patch

from django.conf import settings
from django.test import TestCase

from places.models import AdministrativeAreaLevel1, Place, PlaceManager


class PlaceManagerGetDetailsMethodTest(TestCase):
    def setUp(self):
        self.gmaps_patcher = patch("places.models.cacheable_gmaps")
        self.gmaps_mock = self.gmaps_patcher.start()

    def tearDown(self):
        self.gmaps_patcher.stop()

    def test_call_gmaps_find_place(self):
        address = "sdqdqwdq"

        Place.objects.get_details(address)

        self.gmaps_mock.find_place.assert_called_once_with(
            input=address,
            input_type="textquery",
        )

    def test_response_status_not_eq_OK(self):
        self.gmaps_mock.find_place.return_value = {"status": "wfe"}

        result = Place.objects.get_details("sdqdqwdq")

        self.assertIsNone(result)

    def test_call_get_method_of_manager(self):
        place_id = "place id"
        self.gmaps_mock.find_place.return_value = {
            "status": "OK",
            "candidates": [{"place_id": place_id}],
        }

        with patch.object(Place.objects, "get") as get_mock:
            Place.objects.get_details("sdqdqwdq")

        get_mock.assert_called_once_with(place_id=place_id)

    @patch.object(Place.objects, "get", side_effect=Place.DoesNotExist)
    def test_handle_DoesNotExist_exception(self, _):
        self.gmaps_mock.find_place.return_value = {
            "status": "OK",
            "candidates": [{"place_id": "place_id"}],
        }

        Place.objects.get_details("sdqdqwdq")

    @patch.object(Place.objects, "get", side_effect=Place.DoesNotExist)
    def test_call_gmaps_place(self, _):
        place_id = "place_id"
        self.gmaps_mock.find_place.return_value = {
            "status": "OK",
            "candidates": [{"place_id": place_id}],
        }

        Place.objects.get_details("sdqdqwdq")

        calls = [
            call(place_id, language=lang)
            for lang in settings.MODELTRANSLATION_LANGUAGES
        ]
        self.assertEqual(
            self.gmaps_mock.place.call_count,
            len(settings.MODELTRANSLATION_LANGUAGES),
        )
        self.gmaps_mock.place.assert_has_calls(calls, any_order=True)


class PlaceManagerGetComponentObjectMethodTest(TestCase):
    def setUp(self):
        self.details = {
            "en": {
                "address_components": [
                    {
                        "types": {"administrative_area_level_1"},
                        "long_name": "CanilloLongEn",
                        "short_name": "CanilloShortEn",
                    }
                ],
            },
            "ru": {
                "address_components": [
                    {
                        "types": {"administrative_area_level_1"},
                        "long_name": "CanilloLongRu",
                        "short_name": "CanilloShortRu",
                    }
                ],
            },
            "es": {
                "address_components": [
                    {
                        "types": {"administrative_area_level_1"},
                        "long_name": "CanilloLongEs",
                        "short_name": "CanilloShortEs",
                    }
                ],
            },
        }

    def test_with_empty_details(self):
        with self.assertRaises(KeyError):
            PlaceManager.get_component_object(
                AdministrativeAreaLevel1,
                "administrative_area_level_1",
                {},
            )

    def test_create_related_instance(self):
        result = PlaceManager.get_component_object(
            AdministrativeAreaLevel1,
            "administrative_area_level_1",
            self.details,
        )

        self.assertEqual(AdministrativeAreaLevel1.objects.count(), 1)
        self.assertEqual(result, AdministrativeAreaLevel1.objects.first())
        self.assertEqual(result.long_name, "CanilloLongEn")
        self.assertEqual(result.short_name, "CanilloShortEn")
        self.assertEqual(result.long_name_es, "CanilloLongEs")
        self.assertEqual(result.short_name_es, "CanilloShortEs")
        self.assertEqual(result.long_name_en, "CanilloLongEn")
        self.assertEqual(result.short_name_en, "CanilloShortEn")
        self.assertEqual(result.long_name_ru, "CanilloLongRu")
        self.assertEqual(result.short_name_ru, "CanilloShortRu")

    def test_with_key_arg_that_does_not_exist(self):
        result = PlaceManager.get_component_object(
            AdministrativeAreaLevel1,
            "dummy",
            self.details,
        )

        self.assertIsNone(result)


class PlaceManagerGetFormattedAddressMethodTest(TestCase):
    def test_with_empty_details(self):
        with self.assertRaises(KeyError):
            PlaceManager.get_formatted_address({})

    def test(self):
        en_addr = "en_addr"
        ru_addr = "ru_addr"
        es_addr = "es_addr"
        details = {
            "en": {"formatted_address": en_addr},
            "ru": {"formatted_address": ru_addr},
            "es": {"formatted_address": es_addr},
        }
        expected_result = {
            "formatted_address_en": en_addr,
            "formatted_address_ru": ru_addr,
            "formatted_address_es": es_addr,
        }

        result = PlaceManager.get_formatted_address(details)

        self.assertEqual(result, expected_result)


class PlaceManagerGetCountryCodeMethodTest(TestCase):
    def test_with_empty_details(self):
        with self.assertRaises(KeyError):
            PlaceManager.get_country_code({})

    def test_with_country(self):
        expected_result = "wefuiwehif"
        details = {
            "en": {
                "address_components": [
                    {
                        "types": {},
                        "short_name": "rthrt",
                    },
                    {
                        "types": {"country": "wyukyuk"},
                        "short_name": expected_result,
                    },
                ],
            },
        }

        result = PlaceManager.get_country_code(details)

        self.assertEqual(result, expected_result)

    def test_without_country(self):
        details = {
            "en": {
                "address_components": [
                    {
                        "types": {},
                        "short_name": "wefuiwehif",
                    },
                ],
            },
        }

        with self.assertRaises(StopIteration):
            PlaceManager.get_country_code(details)
