from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class PropertyType(models.Model):
    """
    Property type classification (Apartment, House, Villa, etc.)
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class PropertyStatus(models.Model):
    """
    Property status (Available, Sold, Rented, etc.)
    """
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
        ('withdrawn', 'Withdrawn'),
        ('under_offer', 'Under Offer'),
    )
    
    name = models.CharField(max_length=20, choices=STATUS_CHOICES, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Property Statuses"

    def __str__(self):
        return self.get_name_display()


class Property(models.Model):
    """
    Main Property model
    """
    LISTING_TYPES = (
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
        ('both', 'Sale & Rent'),
    )

    CONDITION_CHOICES = (
        ('new', 'New'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('needs_renovation', 'Needs Renovation'),
    )

    FURNISHING_CHOICES = (
        ('unfurnished', 'Unfurnished'),
        ('semi_furnished', 'Semi Furnished'),
        ('fully_furnished', 'Fully Furnished'),
    )

    # Basic Information
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.ForeignKey(PropertyType, on_delete=models.PROTECT)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPES)
    status = models.ForeignKey(PropertyStatus, on_delete=models.PROTECT)
    
    # Location
    area = models.ForeignKey('locations.Area', on_delete=models.PROTECT, related_name='properties')
    address = models.TextField()
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    
    # Property Details
    bedrooms = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)])
    bathrooms = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)])
    area_sqft = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    area_sqm = models.PositiveIntegerField(blank=True, null=True)
    floor_number = models.IntegerField(blank=True, null=True)
    total_floors = models.PositiveIntegerField(blank=True, null=True)
    parking_spaces = models.PositiveIntegerField(default=0)
    year_built = models.PositiveIntegerField(blank=True, null=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    furnishing = models.CharField(max_length=20, choices=FURNISHING_CHOICES, default='unfurnished')
    
    # Pricing
    price = models.DecimalField(max_digits=12, decimal_places=2)
    price_per_sqft = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, default='USD')
    
    # Ownership & Management
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_properties')
    agent = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='managed_properties',
        limit_choices_to={'user_type': 'agent'}
    )
    
    # Features & Amenities
    has_balcony = models.BooleanField(default=False)
    has_garden = models.BooleanField(default=False)
    has_swimming_pool = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_elevator = models.BooleanField(default=False)
    has_security = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    pet_friendly = models.BooleanField(default=False)
    
    # SEO & Marketing
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=320, blank=True)
    
    # Status & Timestamps
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'listing_type']),
            models.Index(fields=['property_type', 'area']),
            models.Index(fields=['price', 'area_sqft']),
        ]

    def __str__(self):
        return f"{self.title} - {self.area.name}"

    def save(self, *args, **kwargs):
        # Calculate price per sqft
        if self.price and self.area_sqft:
            self.price_per_sqft = self.price / self.area_sqft
        
        # Convert sqft to sqm
        if self.area_sqft and not self.area_sqm:
            self.area_sqm = round(self.area_sqft * 0.092903)
        
        super().save(*args, **kwargs)


class PropertyFeature(models.Model):
    """
    Additional property features/amenities
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['property', 'name']

    def __str__(self):
        return f"{self.property.title} - {self.name}"


class PropertyViewing(models.Model):
    """
    Property viewing appointments
    """
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='viewings')
    viewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='property_viewings')
    agent = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='conducted_viewings',
        limit_choices_to={'user_type': 'agent'}
    )
    scheduled_date = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['scheduled_date']

    def __str__(self):
        return f"{self.property.title} - {self.viewer.full_name} on {self.scheduled_date.date()}"
