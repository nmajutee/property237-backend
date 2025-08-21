from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, UserPreferences, UserVerification
from locations.serializers import CitySerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'email', 'username', 'first_name', 'last_name',
            'phone_number', 'whatsapp_number', 'user_type',
            'city', 'password', 'password_confirm'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        if not (username or email):
            raise serializers.ValidationError('Username or email required')
        if not password:
            raise serializers.ValidationError('Password required')

        # Try authenticate with username first, then email
        user = None
        if username:
            user = authenticate(username=username, password=password)
        if not user and email:
            user = authenticate(username=email, password=password)  # Many auth backends use username field for email too

        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')

        attrs['user'] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'phone_number', 'whatsapp_number', 'user_type', 'city',
            'profile_picture', 'is_phone_verified', 'is_email_verified',
            'is_kyc_verified', 'date_joined'
        ]
        read_only_fields = ['id', 'email', 'date_joined', 'is_phone_verified', 'is_email_verified', 'is_kyc_verified']


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = '__all__'