from otp.otp_admin import admin_site

from .models import (AdministrativeAreaLevel1, AdministrativeAreaLevel2,
                     AdministrativeAreaLevel3, AdministrativeAreaLevel4,
                     AdministrativeAreaLevel5, Locality, Neighborhood, Place,
                     Route, SubLocalityLevel1, SubLocalityLevel2,
                     SubLocalityLevel3, SubLocalityLevel4, SubLocalityLevel5)

models_list = (
    AdministrativeAreaLevel1, AdministrativeAreaLevel2,
    AdministrativeAreaLevel3, AdministrativeAreaLevel4,
    AdministrativeAreaLevel5, Locality, SubLocalityLevel1, SubLocalityLevel2,
    SubLocalityLevel3, SubLocalityLevel4, SubLocalityLevel5, Neighborhood,
    Route, Place
)

for model in models_list:
    admin_site.register(model)
