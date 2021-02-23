from unittest import mock

from core.tests import UserBaseTestCase
from django.utils.crypto import get_random_string
from googlemaps import Client
from rest_framework import status
from rest_framework.reverse import reverse

from .models import Locality, Place


def get_test_place():
    locality = Locality.objects.create(
        long_name='Pirrama Rd', short_name='Pirrama Rd'
    )
    return Place.objects.create(
        place_id=get_random_string(),
        formatted_address='5, 48 Pirrama Rd, Pyrmont NSW 2009, Australia',
        formatted_address_en='5, 48 Pirrama Rd, Pyrmont NSW 2009, Australia',
        formatted_address_ru='5, 48 Пирамида, Пирмонд 2009, Австралия',
        country='AU',
        latitude=-33.866651,
        longitude=151.195827,
        locality=locality
    )


class PlaceAddressAutocompleteViewTests(UserBaseTestCase):
    """
    Tests for PlaceAddressAutocompleteView
    """

    @mock.patch.object(
        Client,
        'places_autocomplete',
        return_value=[{'description': 'New York, NY, USA'}]
    )
    def test_get(self, *args, **kwargs):
        """
        test for get request to places_autocomplete
        :return: 200
        """
        response = self.client.get(reverse('places_autocomplete'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(
            '{}?q=New+York&country_code=US'.format(
                reverse('places_autocomplete')
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'address': 'New York, NY, USA'}])
