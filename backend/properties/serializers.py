from rest_framework import serializers
from .models import PropertyType, PropertyStatus, Property, PropertyFeature, PropertyViewing
from locations.serializers import AreaSerializer
from agentprofile.serializers import AgentProfileSerializer


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ['id', 'name', 'category', 'description', 'is_active']


class PropertyStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyStatus
        fields = ['id', 'name', 'description', 'is_active']


class PropertyFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyFeature
        fields = ['id', 'feature_name', 'feature_value', 'is_highlighted']


class PropertyListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for property listings"""
    property_type = PropertyTypeSerializer(read_only=True)
    status = PropertyStatusSerializer(read_only=True)
    area = AreaSerializer(read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'property_type', 'status', 'listing_type',
            'price', 'currency', 'area', 'no_of_bedrooms', 'no_of_bathrooms',
            'created_at', 'slug', 'featured'
        ]


class PropertyDetailSerializer(serializers.ModelSerializer):
    """Complete property data for detail views"""
    property_type = PropertyTypeSerializer(read_only=True)
    status = PropertyStatusSerializer(read_only=True)
    area = AreaSerializer(read_only=True)
    agent = AgentProfileSerializer(read_only=True)
    additional_features = PropertyFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = '__all__'


class PropertyCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating properties"""
    class Meta:
        model = Property
        exclude = ['created_at', 'updated_at', 'slug', 'views_count']

    def create(self, validated_data):
        # Set the agent from the authenticated user
        if self.context['request'].user.user_type == 'agent':
            validated_data['agent'] = self.context['request'].user.agent_profile
        return super().create(validated_data)


class PropertyViewingSerializer(serializers.ModelSerializer):
    property_listing = PropertyListSerializer(read_only=True)
    viewer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = PropertyViewing
        fields = '__all__'