from unittest.mock import patch

from django.test import TestCase

from places.models import Place, PlaceManager


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
