from django.urls import path
from . import views
from django.http import JsonResponse

def users_api_root(request):
    """Users API root endpoint"""
    return JsonResponse({"message": "Users API is working"})

app_name = 'users'

urlpatterns = [
    # API root
    path('', users_api_root, name='users-root'),

    # Authentication
    path('register/', views.UserRegistrationAPIView.as_view(), name='user-register'),
    path('login/', views.user_login, name='user-login'),
    path('logout/', views.user_logout, name='user-logout'),

    # Profile management
    path('profile/', views.UserProfileAPIView.as_view(), name='user-profile'),
    path('preferences/', views.UserPreferencesAPIView.as_view(), name='user-preferences'),
]