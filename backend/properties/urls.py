from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    # Property CRUD
    path('', views.PropertyListCreateAPIView.as_view(), name='property-list-create'),
    path('<slug:slug>/', views.PropertyDetailAPIView.as_view(), name='property-detail'),
    path('search/', views.property_search, name='property-search'),

    # Property metadata
    path('types/', views.PropertyTypeListAPIView.as_view(), name='property-types'),
    path('statuses/', views.PropertyStatusListAPIView.as_view(), name='property-statuses'),

    # Property viewing
    path('viewings/', views.PropertyViewingCreateAPIView.as_view(), name='property-viewing'),
]