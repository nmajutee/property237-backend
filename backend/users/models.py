from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    """
    Custom User model with Cameroon-specific features
    """
    USER_TYPES = (
        ('client', 'Property Seeker'),
        ('landlord', 'Landlord'),
        ('agent', 'Real Estate Agent'),
        ('admin', 'Admin'),
    )

    PREFERRED_CONTACT = (
        ('whatsapp', 'WhatsApp'),
        ('calls', 'Calls Only'),
        ('both', 'WhatsApp & Calls'),
    )

    # Basic Information
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+237[67]\d{8}$',
        message="Enter a valid Cameroon phone number: +237XXXXXXXXX"
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=13,
        unique=True,
        help_text="Cameroon phone number format: +237XXXXXXXXX"
    )
    whatsapp_number = models.CharField(
        validators=[phone_regex],
        max_length=13,
        blank=True,
        help_text="WhatsApp number (can be different from main phone)"
    )
    preferred_contact_method = models.CharField(
        max_length=10,
        choices=PREFERRED_CONTACT,
        default='both'
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='client')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Location
    city = models.ForeignKey(
        'locations.City',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Primary city location"
    )
    address = models.TextField(blank=True)

    # Verification Status
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_kyc_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)

    # Agent/Landlord Specific
    company_name = models.CharField(max_length=200, blank=True, help_text="Company/Agency name")
    nickname = models.CharField(max_length=100, blank=True, help_text="e.g., Papa Immo")

    # KYC Information
    id_card_number = models.CharField(max_length=50, blank=True)
    id_card_front = models.ImageField(upload_to='kyc_documents/', blank=True, null=True)
    id_card_back = models.ImageField(upload_to='kyc_documents/', blank=True, null=True)

    # Account Status
    is_active = models.BooleanField(default=True)
    is_suspended = models.BooleanField(default=False)
    suspension_reason = models.TextField(blank=True)

    # Timestamps
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']

    def __str__(self):
        return f"{self.email} - {self.get_user_type_display()}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def display_name(self):
        """Return nickname if available, otherwise full name"""
        return self.nickname or self.full_name

    @property
    def verification_badges(self):
        """Return list of verification badges earned"""
        badges = []
        if self.is_phone_verified:
            badges.append('Phone Verified')
        if self.is_email_verified:
            badges.append('Email Verified')
        if self.is_kyc_verified:
            badges.append('Identity Verified')
        return badges

    def can_list_properties(self):
        """Check if user can list properties"""
        return self.user_type in ['agent', 'landlord'] and self.is_phone_verified


class UserPreferences(models.Model):
    """
    User preferences for notifications and Cameroon-specific settings
    """
    LANGUAGES = (
        ('en', 'English'),
        ('fr', 'French'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='preferences')

    # Notifications
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    whatsapp_notifications = models.BooleanField(default=True)
    property_alerts = models.BooleanField(default=True)
    price_drop_alerts = models.BooleanField(default=True)
    newsletter_subscription = models.BooleanField(default=False)

    # Localization
    preferred_language = models.CharField(max_length=2, choices=LANGUAGES, default='en')
    preferred_currency = models.CharField(max_length=3, default='XAF')

    # Search Preferences
    preferred_property_types = models.ManyToManyField(
        'properties.PropertyType',
        blank=True,
        help_text="Preferred property types for alerts"
    )
    max_budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Maximum budget for property alerts"
    )
    preferred_areas = models.ManyToManyField(
        'locations.Area',
        blank=True,
        help_text="Preferred areas for property alerts"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for {self.user.email}"


class UserVerification(models.Model):
    """
    Track verification processes and attempts
    """
    VERIFICATION_TYPES = (
        ('phone', 'Phone Verification'),
        ('email', 'Email Verification'),
        ('kyc', 'KYC Verification'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='verifications')
    verification_type = models.CharField(max_length=10, choices=VERIFICATION_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    verification_code = models.CharField(max_length=10, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_verifications'
    )
    rejection_reason = models.TextField(blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user.email} - {self.get_verification_type_display()} - {self.status}"

    # Custom methods for managing and populating data

    @staticmethod
    def populate_cameroon_locations():
        """
        Populate Cameroon cities and areas.
        This is a placeholder for the actual implementation.
        """
        # Implementation goes here
        pass

    @staticmethod
    def populate_property_types():
        """
        Populate property types.
        This is a placeholder for the actual implementation.
        """
        # Implementation goes here
        pass

# Run the population commands
# python manage.py populate_cameroon_locations
# python manage.py populate_property_types

# Start the server to check admin
# python manage.py runserver