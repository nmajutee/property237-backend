from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Country, Region, City, Area, PopularLocation
from .serializers import (
    CountrySerializer, RegionSerializer, CitySerializer, AreaSerializer,
    LocationTreeSerializer, PopularLocationSerializer
)


class CountryListAPIView(generics.ListAPIView):
    """List all countries"""
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class RegionListAPIView(generics.ListAPIView):
    """List regions, optionally filtered by country"""
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        country_id = self.request.query_params.get('country', None)
        if country_id:
            queryset = queryset.filter(country_id=country_id)
        return queryset


class CityListAPIView(generics.ListAPIView):
    """List cities, optionally filtered by region"""
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        region_id = self.request.query_params.get('region', None)
        if region_id:
            queryset = queryset.filter(region_id=region_id)
        return queryset.order_by('-is_major_city', 'name')


class AreaListAPIView(generics.ListAPIView):
    """List areas, optionally filtered by city"""
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        city_id = self.request.query_params.get('city', None)
        if city_id:
            queryset = queryset.filter(city_id=city_id)
        return queryset.order_by('name')


@api_view(['GET'])
def location_tree(request):
    """Get complete location hierarchy for dropdowns"""
    countries = Country.objects.prefetch_related(
        'regions__cities__areas'
    ).all()

    data = []
    for country in countries:
        country_data = {
            'id': country.id,
            'name': country.name,
            'code': country.code,
            'regions': []
        }

        for region in country.regions.all():
            region_data = {
                'id': region.id,
                'name': region.name,
                'code': region.code,
                'cities': []
            }

            for city in region.cities.all():
                city_data = {
                    'id': city.id,
                    'name': city.name,
                    'is_major_city': city.is_major_city,
                    'areas': [
                        {
                            'id': area.id,
                            'name': area.name,
                            'local_name': area.local_name
                        }
                        for area in city.areas.all()
                    ]
                }
                region_data['cities'].append(city_data)

            country_data['regions'].append(region_data)

        data.append(country_data)

    return Response(data)


class PopularLocationListAPIView(generics.ListAPIView):
    """List popular locations"""
    queryset = PopularLocation.objects.select_related('area__city__region').all()
    serializer_class = PopularLocationSerializer