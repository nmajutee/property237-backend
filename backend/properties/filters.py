import django_filters
from django_filters.filters import RangeFilter
from .models import Property, PropertyType, PropertyStatus


class PropertyFilter(django_filters.FilterSet):
    """Advanced filtering for properties"""

    # Price range filters
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    price_range = RangeFilter(field_name='price')

    # Location filters
    city = django_filters.CharFilter(field_name='area__city__name', lookup_expr='icontains')
    region = django_filters.CharFilter(field_name='area__city__region__name', lookup_expr='icontains')
    area = django_filters.CharFilter(field_name='area__name', lookup_expr='icontains')

    # Property characteristics — use .none() to avoid DB access at import time
    property_type = django_filters.ModelChoiceFilter(queryset=PropertyType.objects.none())
    listing_type = django_filters.ChoiceFilter(choices=Property.LISTING_TYPES)
    status = django_filters.ModelChoiceFilter(queryset=PropertyStatus.objects.none())

    # Room filters
    bedrooms_min = django_filters.NumberFilter(field_name='no_of_bedrooms', lookup_expr='gte')
    bedrooms_max = django_filters.NumberFilter(field_name='no_of_bedrooms', lookup_expr='lte')
    bathrooms_min = django_filters.NumberFilter(field_name='no_of_bathrooms', lookup_expr='gte')

    # Size filters
    land_size_min = django_filters.NumberFilter(field_name='land_size_sqm', lookup_expr='gte')
    land_size_max = django_filters.NumberFilter(field_name='land_size_sqm', lookup_expr='lte')

    # Amenities and utilities
    has_parking = django_filters.BooleanFilter(field_name='has_parking')
    has_pool = django_filters.BooleanFilter(field_name='has_pool')
    has_gym = django_filters.BooleanFilter(field_name='has_gym')
    has_security = django_filters.BooleanFilter(field_name='has_security')
    has_elevator = django_filters.BooleanFilter(field_name='has_elevator')
    has_generator = django_filters.BooleanFilter(field_name='has_generator')
    has_hot_water = django_filters.BooleanFilter(field_name='has_hot_water')
    has_ac_preinstalled = django_filters.BooleanFilter(field_name='has_ac_preinstalled')

    # Utilities
    water_type = django_filters.ChoiceFilter(choices=Property.WATER_TYPES)
    electricity_type = django_filters.ChoiceFilter(choices=Property.ELECTRICITY_TYPES)
    vehicle_access = django_filters.ChoiceFilter(choices=Property.VEHICLE_ACCESS)

    # Property specific filters
    road_is_tarred = django_filters.BooleanFilter(field_name='road_is_tarred')
    has_land_title = django_filters.BooleanFilter(field_name='has_land_title')

    # Special filters
    featured = django_filters.BooleanFilter(field_name='featured')
    is_active = django_filters.BooleanFilter(field_name='is_active')

    # Agent filters
    agent = django_filters.CharFilter(field_name='agent__user__username', lookup_expr='icontains')

    # Date filters
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Property
        fields = {
            'title': ['icontains'],
            'description': ['icontains'],
            'currency': ['exact'],
            'no_of_floors': ['exact', 'gte', 'lte'],
            'no_of_bedrooms': ['exact', 'gte', 'lte'],
            'no_of_bathrooms': ['exact', 'gte', 'lte'],
            'price': ['exact', 'gte', 'lte'],
            'land_size_sqm': ['exact', 'gte', 'lte'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Safely populate querysets without causing import loops
        if 'property_type' in self.filters:
            self.filters['property_type'].queryset = PropertyType.objects.filter(is_active=True)
        if 'status' in self.filters:
            self.filters['status'].queryset = PropertyStatus.objects.filter(is_active=True)