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


class State(models.Model):
    """
    State/Province model
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['name', 'country']
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class City(models.Model):
    """
    City model
    """
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
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
        unique_together = ['name', 'state']
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.state.name}"


class Area(models.Model):
    """
    Area/Neighborhood model within cities
    """
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='areas')
    description = models.TextField(blank=True)
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
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['name', 'city']
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.city.name}"
