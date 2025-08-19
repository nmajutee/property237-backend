from rest_framework import serializers
from .models import MediaFile


class MediaFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = MediaFile
        fields = [
            'id', 'file', 'file_url', 'file_type', 'title', 'description',
            'order', 'is_featured', 'uploaded_at'
        ]
        read_only_fields = ['id', 'uploaded_at']

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None

    def validate_file(self, value):
        # Validate file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 10MB")

        # Validate file type based on extension
        allowed_extensions = {
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
            'video': ['.mp4', '.avi', '.mov', '.wmv'],
            'document': ['.pdf', '.doc', '.docx', '.txt']
        }

        file_name = value.name.lower()
        file_type = self.initial_data.get('file_type', 'image')

        if file_type in allowed_extensions:
            valid_extensions = allowed_extensions[file_type]
            if not any(file_name.endswith(ext) for ext in valid_extensions):
                raise serializers.ValidationError(
                    f"Invalid file type for {file_type}. "
                    f"Allowed: {', '.join(valid_extensions)}"
                )

        return value