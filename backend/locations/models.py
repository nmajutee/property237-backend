from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Country(models.Model):
    """
    Country model for geographic organization
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True)  # ISO country code
    phone_code = models.CharField(max_length=5, blank=True)
    currency = models.CharField(max_length=3, blank=True)  # Currency code
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']

    def __str__(self):
        return self.name


class Region(models.Model):
    """
    Cameroon Regions (replacing State for local context)
    """
    CAMEROON_REGIONS = (
        ('centre', 'Centre'),
        ('littoral', 'Littoral'),
        ('northwest', 'Northwest'),
        ('southwest', 'Southwest'),
        ('west', 'West'),
        ('adamawa', 'Adamawa'),
        ('east', 'East'),
        ('far_north', 'Far North'),
        ('north', 'North'),
        ('south', 'South'),
    )

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, choices=CAMEROON_REGIONS, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='regions')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['name', 'country']
        ordering = ['name']

    def __str__(self):
        return f"{self.name} Region"


class City(models.Model):
    """
    Major cities in Cameroon
    """
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities')
    is_major_city = models.BooleanField(default=False, help_text="Major cities like Douala, Yaoundé")
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
    population = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Cities"
        unique_together = ['name', 'region']
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.region.name}"


class Area(models.Model):
    """
    Quarters/Neighborhoods within cities (Cameroon-specific)
    """
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='areas')
    local_name = models.CharField(max_length=100, blank=True, help_text="Local/French name")
    description = models.TextField(blank=True)

    # Area characteristics
    is_residential = models.BooleanField(default=True)
    is_commercial = models.BooleanField(default=False)
    is_industrial = models.BooleanField(default=False)

    # Infrastructure
    has_tarred_roads = models.BooleanField(default=False)
    has_electricity = models.BooleanField(default=True)
    has_water_supply = models.BooleanField(default=True)

    # Location data
    postal_code = models.CharField(max_length=20, blank=True)
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

    # Administrative
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['name', 'city']
        ordering = ['city__name', 'name']

    def __str__(self):
        return f"{self.name}, {self.city.name}"

    @property
    def full_location(self):
        return f"{self.name}, {self.city.name}, {self.city.region.name}"


class PopularLocation(models.Model):
    """
    Track popular/trending areas for better UX
    """
    area = models.OneToOneField(Area, on_delete=models.CASCADE, related_name='popularity_stats')
    property_count = models.PositiveIntegerField(default=0)
    search_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    is_trending = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-property_count', '-search_count']

    def __str__(self):
        return f"{self.area.name} - {self.property_count} properties"