"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/properties/', include('properties.urls')),
    path('api/users/', include('users.urls')),
    path('api/locations/', include('locations.urls')),
    path('api/agents/', include('agentprofile.urls')),
    path('api/media/', include('media.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)