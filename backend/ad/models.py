from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class AdPackage(models.Model):
    """
    Different advertising packages available
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    duration_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    # Features
    featured_listing = models.BooleanField(default=False)
    priority_placement = models.BooleanField(default=False)
    social_media_boost = models.BooleanField(default=False)
    email_marketing = models.BooleanField(default=False)
    analytics_access = models.BooleanField(default=False)
    max_photos = models.PositiveIntegerField(default=10)
    max_videos = models.PositiveIntegerField(default=1)
    virtual_tour_included = models.BooleanField(default=False)

    # Display settings
    display_order = models.PositiveIntegerField(default=0)
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'price']

    def __str__(self):
        return f"{self.name} - {self.duration_days} days"


class Advertisement(models.Model):
    """
    Property advertisements
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('expired', 'Expired'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )

    PLACEMENT_CHOICES = (
        ('homepage', 'Homepage'),
        ('search_results', 'Search Results'),
        ('property_detail', 'Property Detail'),
        ('sidebar', 'Sidebar'),
        ('footer', 'Footer'),
        ('newsletter', 'Newsletter'),
        ('social_media', 'Social Media'),
    )

    property_listing = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='advertisements')
    advertiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertisements')
    package = models.ForeignKey('ad.AdPackage', on_delete=models.PROTECT)

    # Advertisement Details
    title = models.CharField(max_length=200)
    description = models.TextField()
    call_to_action = models.CharField(max_length=50, default="View Details")
    target_url = models.URLField(blank=True)

    # Placement & Targeting
    placement = models.CharField(max_length=20, choices=PLACEMENT_CHOICES, default='search_results')
    target_audience = models.TextField(blank=True, help_text="Target audience description")

    # Scheduling
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')

    # Budget & Billing
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    payment_status = models.CharField(
        max_length=15,
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('partial', 'Partially Paid'),
            ('refunded', 'Refunded'),
        ],
        default='pending'
    )

    # Performance Metrics
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    conversions = models.PositiveIntegerField(default=0)

    # Admin fields
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_ads',
        limit_choices_to={'user_type': 'admin'}
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.property_listing.title}"

    @property
    def click_through_rate(self):
        if self.impressions > 0:
            return (self.clicks / self.impressions) * 100
        return 0

    @property
    def conversion_rate(self):
        if self.clicks > 0:
            return (self.conversions / self.clicks) * 100
        return 0

    @property
    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return (
            self.status == 'active' and
            self.start_date <= now <= self.end_date and
            self.payment_status == 'paid'
        )


class AdImpression(models.Model):
    """
    Track ad impressions for analytics
    """
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='impression_logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    referrer = models.URLField(blank=True)
    page_url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.advertisement.title} - {self.timestamp}"


class AdClick(models.Model):
    """
    Track ad clicks for analytics
    """
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='click_logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    referrer = models.URLField(blank=True)
    destination_url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.advertisement.title} - Click at {self.timestamp}"


class AdBanner(models.Model):
    """
    Banner advertisements (not tied to specific properties)
    """
    BANNER_SIZES = (
        ('728x90', 'Leaderboard (728x90)'),
        ('300x250', 'Medium Rectangle (300x250)'),
        ('320x50', 'Mobile Banner (320x50)'),
        ('160x600', 'Wide Skyscraper (160x600)'),
        ('300x600', 'Half Page (300x600)'),
        ('970x250', 'Large Leaderboard (970x250)'),
    )

    advertiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='banner_ads')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banner_ads/')
    link_url = models.URLField()
    alt_text = models.CharField(max_length=200)
    size = models.CharField(max_length=10, choices=BANNER_SIZES)
    placement = models.CharField(max_length=20, choices=Advertisement.PLACEMENT_CHOICES)

    # Scheduling
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    # Pricing
    cost_per_impression = models.DecimalField(max_digits=6, decimal_places=4, default=0.001)
    cost_per_click = models.DecimalField(max_digits=6, decimal_places=2, default=0.50)
    max_budget = models.DecimalField(max_digits=10, decimal_places=2)
    spent_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Metrics
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.size}"


class PromotedProperty(models.Model):
    """
    Properties promoted to appear in special sections
    """
    PROMOTION_TYPES = (
        ('featured', 'Featured Property'),
        ('hot_deal', 'Hot Deal'),
        ('price_reduced', 'Price Reduced'),
        ('new_listing', 'New Listing'),
        ('urgent_sale', 'Urgent Sale'),
        ('premium', 'Premium Listing'),
    )

    property_listing = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='promotions')
    agent = models.ForeignKey('agentprofile.AgentProfile', on_delete=models.CASCADE, related_name='promoted_properties')
    promotion_type = models.CharField(max_length=15, choices=PROMOTION_TYPES)

    # Scheduling
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    # Pricing
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    # Display
    priority_score = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    badge_text = models.CharField(max_length=50, blank=True)
    highlight_color = models.CharField(max_length=7, default="#FF6B35")  # Hex color

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority_score', '-created_at']

    def __str__(self):
        return f"{self.property_listing.title} - {self.get_promotion_type_display()}"
