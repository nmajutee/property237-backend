from rest_framework import serializers
from .models import AgentProfile, AgentCertification, AgentReview
from users.serializers import UserProfileSerializer
from locations.serializers import AreaSerializer


class AgentProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    service_areas = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = AgentProfile
        fields = [
            'id', 'user', 'license_number', 'agency_name', 'years_experience',
            'specialization', 'bio', 'service_areas', 'is_verified', 'is_featured',
            'total_sales', 'total_rentals', 'client_rating', 'total_reviews'
        ]


class AgentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProfile
        fields = [
            'license_number', 'license_expiry', 'agency_name', 'agency_address',
            'years_experience', 'specialization', 'office_phone', 'website',
            'bio', 'languages_spoken'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class AgentCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentCertification
        fields = '__all__'


class AgentReviewSerializer(serializers.ModelSerializer):
    reviewer = UserProfileSerializer(read_only=True)

    class Meta:
        model = AgentReview
        fields = '__all__'
        read_only_fields = ['reviewer', 'created_at', 'updated_at']