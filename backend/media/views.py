from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import MediaFile
from .serializers import MediaFileSerializer


class MediaFileUploadAPIView(generics.CreateAPIView):
    """Upload media files (images, videos, documents)"""
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class MediaFileListAPIView(generics.ListAPIView):
    """List media files for a property"""
    serializer_class = MediaFileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        property_id = self.kwargs.get('property_id')
        return MediaFile.objects.filter(
            property_id=property_id,
            is_active=True
        ).order_by('file_type', 'order')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_media_file(request, file_id):
    """Delete a media file"""
    try:
        media_file = MediaFile.objects.get(
            id=file_id,
            uploaded_by=request.user
        )
        media_file.is_active = False
        media_file.save()
        return Response({'message': 'File deleted successfully'})
    except MediaFile.DoesNotExist:
        return Response(
            {'error': 'File not found or permission denied'},
            status=status.HTTP_404_NOT_FOUND
        )