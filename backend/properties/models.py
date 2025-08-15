from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class PropertyType(models.Model):
    """
    Cameroon-specific property classifications
    """
    PROPERTY_CATEGORIES = (
        ('chambre_modern', 'Chambre Modern/Room'),
        ('studio', 'Studio'),
        ('apartment', 'Apartment'),
        ('bungalow', 'Bungalow'),
        ('villa_duplex', 'Villa/Duplex'),
        ('commercial', 'Commercial Property/Office/Shop'),
        ('land', 'Land'),
        ('warehouse', 'Warehouse'),
        ('guest_house', 'Guest House'),
    )

    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=PROPERTY_CATEGORIES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class PropertyStatus(models.Model):
    """
    Property availability status
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
    Main Property model with Cameroon-specific features
    """
    LISTING_TYPES = (
        ('rent', 'For Rent'),
        ('sale', 'For Sale'),
        ('guest_house', 'Guest House'),
    )

    ELECTRICITY_TYPES = (
        ('private_meter', 'Private Meter'),
        ('shared_meter', 'Shared Meter'),
    )

    ELECTRICITY_PAYMENT = (
        ('prepaid', 'Prepaid'),
        ('postpaid', 'Postpaid'),
    )

    WATER_TYPES = (
        ('camwater', 'Camwater'),
        ('forage', 'Forage/Borehole'),
    )

    KITCHEN_TYPES = (
        ('full_size', 'Full Size Kitchen'),
        ('partial', 'Partial/Corner Kitchen'),
    )

    LAND_TYPES = (
        ('family_land', 'Family Land'),
        ('private_land', 'Private Land'),
        ('community_land', 'Community Land'),
        ('reclaimed_land', 'Reclaimed Land'),
    )

    AREA_CHARACTERISTICS = (
        ('swampy', 'Swampy'),
        ('dry', 'Dry'),
        ('forest_area', 'Forest Area'),
    )

    VEHICLE_ACCESS = (
        ('bike', 'Reachable by Bike'),
        ('low_car', 'Reachable by Low Car/Sedan'),
        ('suv', 'Reachable by SUV'),
    )

    # Basic Information
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.ForeignKey(PropertyType, on_delete=models.PROTECT)
    status = models.ForeignKey(PropertyStatus, on_delete=models.PROTECT)
    listing_type = models.CharField(max_length=15, choices=LISTING_TYPES)

    # Location
    area = models.ForeignKey('locations.Area', on_delete=models.PROTECT)
    google_pin_location = models.TextField(blank=True, help_text="Google Maps pin drop coordinates")
    distance_from_main_road = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Distance in meters"
    )
    road_is_tarred = models.BooleanField(default=False)
    vehicle_access = models.CharField(
        max_length=20,
        choices=VEHICLE_ACCESS,
        blank=True,
        help_text="Best vehicle access type"
    )

    # Property Details
    no_of_bedrooms = models.PositiveIntegerField(default=0)
    no_of_living_rooms = models.PositiveIntegerField(default=0, help_text="Number of parlours/living rooms")
    no_of_bathrooms = models.PositiveIntegerField(default=1)
    no_of_kitchens = models.PositiveIntegerField(default=1)
    kitchen_type = models.CharField(max_length=15, choices=KITCHEN_TYPES, blank=True)
    no_of_balconies = models.PositiveIntegerField(default=0)
    no_of_floors = models.PositiveIntegerField(default=1)
    floor_number = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Which floor is the apartment on (for apartments)"
    )

    # Room specifications
    room_size = models.CharField(max_length=50, blank=True, help_text="e.g., '3m x 4m'")
    has_dressing_cupboard = models.BooleanField(default=False)

    # Utilities
    electricity_type = models.CharField(max_length=15, choices=ELECTRICITY_TYPES, blank=True)
    electricity_payment = models.CharField(max_length=10, choices=ELECTRICITY_PAYMENT, blank=True)
    water_type = models.CharField(max_length=15, choices=WATER_TYPES, blank=True)
    has_ac_preinstalled = models.BooleanField(default=False)
    has_hot_water = models.BooleanField(default=False)
    has_generator = models.BooleanField(default=False)

    # Amenities
    has_parking = models.BooleanField(default=False, help_text="In-fence parking")
    has_security = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_elevator = models.BooleanField(default=False)

    # Pricing
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='XAF')

    # For Rent specific
    initial_months_payable = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Number of months payable at entry"
    )
    caution_months = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Number of months as caution/deposit"
    )
    visit_fee = models.DecimalField(
        max_digits=8, decimal_places=2,
        null=True, blank=True,
        help_text="Fee for property viewing"
    )
    requires_contract_registration = models.BooleanField(default=False)

    # For Sale specific
    land_size_sqm = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text="Land size in square meters"
    )
    has_land_title = models.BooleanField(default=False)
    land_title_type = models.CharField(
        max_length=20,
        choices=[
            ('global', 'Global Land Title'),
            ('extract', 'Personal/Extract Land Title'),
        ],
        blank=True
    )
    other_documentation = models.TextField(blank=True)

    # For Land specific
    land_type = models.CharField(max_length=20, choices=LAND_TYPES, blank=True)
    area_characteristics = models.CharField(max_length=15, choices=AREA_CHARACTERISTICS, blank=True)

    # For Warehouse specific
    warehouse_height = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        help_text="Height in meters"
    )
    has_forklift = models.BooleanField(default=False)
    allows_truck_entry = models.BooleanField(default=False)
    has_inventory_manager = models.BooleanField(default=False)
    requires_goods_documentation = models.BooleanField(default=False)

    # For Guest House specific
    price_per_day = models.DecimalField(
        max_digits=8, decimal_places=2,
        null=True, blank=True
    )
    price_negotiable = models.BooleanField(default=False)
    has_refundable_caution = models.BooleanField(default=False)

    # Agent Information
    agent = models.ForeignKey(
        'agentprofile.AgentProfile',
        on_delete=models.CASCADE,
        related_name='properties'
    )
    agent_commission_percentage = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        help_text="Agent commission as percentage"
    )
    agent_commission_months = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Agent commission in months of rent"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    # SEO and Marketing
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_listing_type_display()}"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(f"{self.title}-{self.area.name}")
        super().save(*args, **kwargs)


class PropertyFeature(models.Model):
    """
    Additional property features and amenities
    """
    property_listing = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='additional_features')
    feature_name = models.CharField(max_length=100)
    feature_value = models.CharField(max_length=200, blank=True)
    is_highlighted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.property_listing.title} - {self.feature_name}"


class PropertyViewing(models.Model):
    """
    Property viewing appointments
    """
    VIEWING_STATUS = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )

    property_listing = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='viewings')
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField()
    status = models.CharField(max_length=15, choices=VIEWING_STATUS, default='scheduled')
    notes = models.TextField(blank=True)
    visit_fee_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_date']

    def __str__(self):
        return f"{self.property_listing.title} - {self.viewer.username} - {self.scheduled_date}"