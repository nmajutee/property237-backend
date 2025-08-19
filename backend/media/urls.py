from django.urls import path
from . import views

app_name = 'media'

urlpatterns = [
    # Media file management
    path('upload/', views.MediaFileUploadAPIView.as_view(), name='media-upload'),
    path('property/<int:property_id>/', views.MediaFileListAPIView.as_view(), name='media-list'),
    path('<int:file_id>/delete/', views.delete_media_file, name='media-delete'),
]