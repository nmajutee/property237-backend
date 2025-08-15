from django.contrib import admin
from .models import Country, Region, City, Area


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'phone_code', 'currency', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'country', 'is_active']
    list_filter = ['country', 'is_active']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'is_major_city', 'is_active']
    list_filter = ['region', 'is_major_city', 'is_active']
    search_fields = ['name']
    readonly_fields = ['created_at']


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'is_residential', 'has_tarred_roads', 'is_active']
    list_filter = ['city', 'is_residential', 'is_commercial', 'has_tarred_roads', 'has_electricity', 'has_water_supply', 'is_active']
    search_fields = ['name', 'local_name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'city', 'local_name', 'description')
        }),
        ('Area Type', {
            'fields': ('is_residential', 'is_commercial', 'is_industrial')
        }),
        ('Infrastructure', {
            'fields': ('has_tarred_roads', 'has_electricity', 'has_water_supply')
        }),
        ('Location', {
            'fields': ('postal_code', 'latitude', 'longitude')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )