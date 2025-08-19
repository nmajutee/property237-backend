from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from utils.permissions import IsAgentOrReadOnly, IsOwnerOrReadOnly
from .models import Property, PropertyType, PropertyStatus, PropertyViewing
from .serializers import (
    PropertyListSerializer, PropertyDetailSerializer, PropertyCreateSerializer,
    PropertyTypeSerializer, PropertyStatusSerializer, PropertyViewingSerializer
)
from .filters import PropertyFilter


class PropertyListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List properties with filtering, search, and pagination
    POST: Create new property (authenticated agents only)
    """
    permission_classes = [IsAgentOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['title', 'description', 'area__name', 'area__city__name']
    ordering_fields = ['price', 'created_at', 'views_count']
    ordering = ['-created_at']

    def get_queryset(self):
        return Property.objects.filter(is_active=True).select_related(
            'property_type', 'status', 'area__city__region', 'agent__user'
        ).prefetch_related('additional_features', 'media_files').order_by('-created_at')  # media_files is now available

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PropertyCreateSerializer
        return PropertyListSerializer

    def perform_create(self, serializer):
        # Ensure only agents can create properties
        if self.request.user.user_type == 'agent':
            serializer.save(agent=self.request.user.agent_profile)
        else:
            raise PermissionError("Only agents can create properties")


class PropertyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Property detail with full information
    PUT/PATCH: Update property (owner/agent only)
    DELETE: Delete property (owner/agent only)
    """
    queryset = Property.objects.select_related(
        'property_type', 'status', 'area__city__region', 'agent__user'
    ).prefetch_related('additional_features', 'media_files')  # media_files now available
    serializer_class = PropertyDetailSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        obj = super().get_object()
        # Increment views count for GET requests (only for anonymous users)
        if self.request.method == 'GET' and not self.request.user.is_authenticated:
            obj.views_count += 1
            obj.save(update_fields=['views_count'])
        return obj

    def perform_update(self, serializer):
        # Only property owner or admin can update
        property_obj = self.get_object()
        if (self.request.user == property_obj.agent.user or
            self.request.user.is_staff):
            serializer.save()
        else:
            raise PermissionError("You can only update your own properties")

    def perform_destroy(self, instance):
        # Soft delete - mark as inactive
        if (self.request.user == instance.agent.user or
            self.request.user.is_staff):
            instance.is_active = False
            instance.save()
        else:
            raise PermissionError("You can only delete your own properties")


@api_view(['GET'])
def property_search(request):
    """Advanced property search with multiple filters"""
    properties = Property.objects.filter(is_active=True)

    # Apply filters
    filterset = PropertyFilter(request.GET, queryset=properties)
    if filterset.is_valid():
        properties = filterset.qs

    # Serialize results
    serializer = PropertyListSerializer(properties, many=True)
    return Response({
        'count': properties.count(),
        'results': serializer.data
    })


class PropertyTypeListAPIView(generics.ListAPIView):
    """List all active property types"""
    queryset = PropertyType.objects.filter(is_active=True)
    serializer_class = PropertyTypeSerializer


class PropertyStatusListAPIView(generics.ListAPIView):
    """List all active property statuses"""
    queryset = PropertyStatus.objects.filter(is_active=True)
    serializer_class = PropertyStatusSerializer


class PropertyViewingCreateAPIView(generics.CreateAPIView):
    """Schedule property viewing"""
    queryset = PropertyViewing.objects.all()
    serializer_class = PropertyViewingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(viewer=self.request.user)