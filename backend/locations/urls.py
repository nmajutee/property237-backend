from django.urls import path
from . import views

app_name = 'locations'

urlpatterns = [
    # Location hierarchy
    path('countries/', views.CountryListAPIView.as_view(), name='country-list'),
    path('regions/', views.RegionListAPIView.as_view(), name='region-list'),
    path('cities/', views.CityListAPIView.as_view(), name='city-list'),
    path('areas/', views.AreaListAPIView.as_view(), name='area-list'),

    # Special endpoints
    path('tree/', views.location_tree, name='location-tree'),
    path('popular/', views.PopularLocationListAPIView.as_view(), name='popular-locations'),
]