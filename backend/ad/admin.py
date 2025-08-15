from django.contrib import admin
from .models import AdPackage, Advertisement, AdImpression, AdClick, AdBanner, PromotedProperty


@admin.register(AdPackage)
class AdPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration_days', 'price', 'currency', 'is_active']
    list_filter = ['currency', 'is_active', 'featured_listing', 'priority_placement']
    search_fields = ['name', 'description']


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'advertiser', 'package', 'status', 'start_date', 'end_date']
    list_filter = ['status', 'package', 'placement', 'payment_status']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AdBanner)
class AdBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'advertiser', 'size', 'placement', 'is_active', 'start_date', 'end_date']
    list_filter = ['size', 'placement', 'is_active']
    search_fields = ['title', 'alt_text']


@admin.register(PromotedProperty)
class PromotedPropertyAdmin(admin.ModelAdmin):
    list_display = ['property_listing', 'agent', 'promotion_type', 'start_date', 'end_date', 'is_active']
    list_filter = ['promotion_type', 'is_active']
    search_fields = ['property_listing__title', 'badge_text']


@admin.register(AdImpression)
class AdImpressionAdmin(admin.ModelAdmin):
    list_display = ['advertisement', 'user', 'timestamp', 'ip_address']
    list_filter = ['timestamp']
    readonly_fields = ['timestamp']


@admin.register(AdClick)
class AdClickAdmin(admin.ModelAdmin):
    list_display = ['advertisement', 'user', 'timestamp', 'ip_address']
    list_filter = ['timestamp']
    readonly_fields = ['timestamp']
