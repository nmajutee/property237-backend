from rest_framework import serializers
from .models import Country, Region, City, Area, PopularLocation


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'phone_code', 'currency']


class RegionSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = Region
        fields = ['id', 'name', 'code', 'country']


class CitySerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'region', 'is_major_city', 'latitude', 'longitude']


class AreaSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    full_location = serializers.ReadOnlyField()

    class Meta:
        model = Area
        fields = [
            'id', 'name', 'local_name', 'city', 'full_location',
            'is_residential', 'is_commercial', 'has_tarred_roads',
            'has_electricity', 'has_water_supply'
        ]


class LocationTreeSerializer(serializers.ModelSerializer):
    """Hierarchical location data for dropdowns"""
    regions = RegionSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ['id', 'name', 'regions']


class PopularLocationSerializer(serializers.ModelSerializer):
    area = AreaSerializer(read_only=True)

    class Meta:
        model = PopularLocation
        fields = ['area', 'property_count', 'is_trending']