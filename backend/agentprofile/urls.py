from django.urls import path
from . import views

app_name = 'agentprofile'

urlpatterns = [
    # Agent registration and profile
    path('register/', views.AgentRegistrationAPIView.as_view(), name='agent-register'),
    path('profile/', views.AgentProfileAPIView.as_view(), name='agent-profile'),

    # Agent listing and details
    path('', views.AgentListAPIView.as_view(), name='agent-list'),
    path('<int:id>/', views.AgentDetailAPIView.as_view(), name='agent-detail'),

    # Agent certifications
    path('certifications/', views.AgentCertificationListCreateAPIView.as_view(), name='agent-certifications'),

    # Agent reviews
    path('<int:agent_id>/reviews/', views.AgentReviewListCreateAPIView.as_view(), name='agent-reviews'),
]