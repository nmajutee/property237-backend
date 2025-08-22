from django.contrib import admin
from .models import Property, PropertyType, PropertyStatus

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active']

@admin.register(PropertyStatus)
class PropertyStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'listing_type', 'price', 'status']
    readonly_fields = ['slug', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'property_type', 'listing_type', 'status')
        }),
        ('Pricing', {
            'fields': ('price',)
        }),
        ('Details', {
            'fields': ('no_of_bedrooms', 'no_of_bathrooms', 'area')
        }),
    )