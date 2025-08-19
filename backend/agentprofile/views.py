from utils.permissions import IsAgentOrReadOnly, IsVerifiedAgent
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import AgentProfile, AgentCertification, AgentReview
from .serializers import (
    AgentProfileSerializer, AgentRegistrationSerializer,
    AgentCertificationSerializer, AgentReviewSerializer
)


class AgentRegistrationAPIView(generics.CreateAPIView):
    """Register as an agent"""
    queryset = AgentProfile.objects.all()
    serializer_class = AgentRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Check if user already has an agent profile
        if hasattr(request.user, 'agent_profile'):
            return Response(
                {'error': 'User already has an agent profile'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update user type to agent
        request.user.user_type = 'agent'
        request.user.save()

        return super().create(request, *args, **kwargs)


class AgentProfileAPIView(generics.RetrieveUpdateAPIView):
    """Get and update agent profile"""
    serializer_class = AgentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.agent_profile


class AgentListAPIView(generics.ListAPIView):
    """List all verified agents"""
    queryset = AgentProfile.objects.filter(
        is_verified=True
    ).select_related('user').prefetch_related('service_areas')
    serializer_class = AgentProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by specialization
        specialization = self.request.query_params.get('specialization', None)
        if specialization:
            queryset = queryset.filter(specialization__icontains=specialization)

        # Filter by service area
        area = self.request.query_params.get('area', None)
        if area:
            queryset = queryset.filter(service_areas__id=area)

        # Filter featured agents
        featured = self.request.query_params.get('featured', None)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)

        return queryset.order_by('-is_featured', '-client_rating', '-total_sales')


class AgentDetailAPIView(generics.RetrieveAPIView):
    """Get agent details by ID"""
    queryset = AgentProfile.objects.filter(is_verified=True)
    serializer_class = AgentProfileSerializer
    lookup_field = 'id'


class AgentCertificationListCreateAPIView(generics.ListCreateAPIView):
    """List and create agent certifications"""
    serializer_class = AgentCertificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AgentCertification.objects.filter(
            agent=self.request.user.agent_profile
        )

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user.agent_profile)


class AgentReviewListCreateAPIView(generics.ListCreateAPIView):
    """List and create agent reviews"""
    serializer_class = AgentReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        agent_id = self.kwargs.get('agent_id')
        return AgentReview.objects.filter(agent_id=agent_id)

    def perform_create(self, serializer):
        agent_id = self.kwargs.get('agent_id')
        serializer.save(
            agent_id=agent_id,
            reviewer=self.request.user
        )