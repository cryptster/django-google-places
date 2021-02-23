from django.urls import path

from .views import PlaceAddressAutocompleteView


urlpatterns = [
    path(
        'places/autocomplete/',
        PlaceAddressAutocompleteView.as_view(),
        name='places_autocomplete'
    ),
]
