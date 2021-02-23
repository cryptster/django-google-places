from rest_framework import views, status
from rest_framework.response import Response

from django.conf import settings

from . import redis_conn

import googlemaps
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from random import random
import pickle


class PlaceAddressAutocompleteView(views.APIView):
    """
    Endpoint for autocomplete addresses from google place
    """

    # swagger manual params
    q_param = openapi.Parameter(
        'q',
        in_=openapi.IN_QUERY,
        description='address',
        type=openapi.TYPE_STRING,
        required=True
    )
    country_code_param = openapi.Parameter(
        'country_code',
        in_=openapi.IN_QUERY,
        description='country code',
        type=openapi.TYPE_STRING,
        required=True
    )

    @swagger_auto_schema(
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING)
            )
        },
        manual_parameters=[q_param, country_code_param]
    )
    def get(self, request, *args, **kwargs):
        """
        Get lists of addresses from google place
        """
        q = request.GET.get('q')
        country_code = request.GET.get('country_code')

        if not q or not country_code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        results = redis_conn.get(
            'places_autocomplete::{}::{}'.format(country_code, q)
        )
        if not results:
            gmaps = googlemaps.Client(key=settings.GOOGLE_PLACES_API_KEY)
            addresses = gmaps.places_autocomplete(
                q, str(random()),
                language=request.user.profile.current_lang,
                components={'country': [country_code]}
            )

            if not addresses:
                return Response()

            results = [{'address': x['description']} for x in addresses]
            pickled_object = pickle.dumps(results)

            redis_conn.set(
                'places_autocomplete::{}'.format(q), pickled_object
            )
            redis_conn.expire(
                'places_autocomplete::{}'.format(q), 60 * 60 * 24
            )
        else:
            results = pickle.loads(results)

        return Response(results)
