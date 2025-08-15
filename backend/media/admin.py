from django.contrib import admin
from .models import MediaCategory, PropertyImage, PropertyVideo, PropertyDocument, VirtualTour, MediaGallery, MediaTag

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property','title','image_type','is_primary','order')
    list_filter = ('image_type','is_primary','is_featured')
    search_fields = ('property__title','title')

admin.site.register(MediaCategory)
admin.site.register(PropertyVideo)
admin.site.register(PropertyDocument)
admin.site.register(VirtualTour)
admin.site.register(MediaGallery)
admin.site.register(MediaTag)
