from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class TariffCategory(models.Model):
    """
    Categories for tariff plans (Agent, Property Owner, Premium, etc.)
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    target_audience = models.CharField(
        max_length=20,
        choices=[
            ('agents', 'Real Estate Agents'),
            ('owners', 'Property Owners'),
            ('developers', 'Property Developers'),
            ('agencies', 'Real Estate Agencies'),
            ('individuals', 'Individual Users'),
        ]
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Tariff Categories"
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class TariffPlan(models.Model):
    """
    Subscription plans for different user types
    """
    BILLING_CYCLES = (
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annual', 'Semi-Annual'),
        ('annual', 'Annual'),
        ('lifetime', 'Lifetime'),
    )

    PLAN_TYPES = (
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    )

    # Basic Information
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    category = models.ForeignKey(TariffCategory, on_delete=models.CASCADE, related_name='plans')
    plan_type = models.CharField(max_length=15, choices=PLAN_TYPES)

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, default='USD')
    billing_cycle = models.CharField(max_length=15, choices=BILLING_CYCLES)

    # Trial & Setup
    trial_days = models.PositiveIntegerField(default=0)
    setup_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    # Property Limits
    max_properties = models.PositiveIntegerField(default=1)
    max_photos_per_property = models.PositiveIntegerField(default=5)
    max_videos_per_property = models.PositiveIntegerField(default=0)
    max_virtual_tours = models.PositiveIntegerField(default=0)
    max_featured_properties = models.PositiveIntegerField(default=0)

    # Advertisement Features
    max_ad_campaigns = models.PositiveIntegerField(default=0)
    max_promoted_properties = models.PositiveIntegerField(default=0)
    social_media_posting = models.BooleanField(default=False)
    email_marketing = models.BooleanField(default=False)

    # Analytics & Reports
    basic_analytics = models.BooleanField(default=True)
    advanced_analytics = models.BooleanField(default=False)
    custom_reports = models.BooleanField(default=False)
    export_data = models.BooleanField(default=False)

    # Support Features
    email_support = models.BooleanField(default=True)
    phone_support = models.BooleanField(default=False)
    priority_support = models.BooleanField(default=False)
    dedicated_manager = models.BooleanField(default=False)

    # API & Integration
    api_access = models.BooleanField(default=False)
    api_calls_per_month = models.PositiveIntegerField(default=0)
    webhook_support = models.BooleanField(default=False)
    third_party_integrations = models.BooleanField(default=False)

    # Branding & Customization
    remove_branding = models.BooleanField(default=False)
    custom_domain = models.BooleanField(default=False)
    custom_themes = models.BooleanField(default=False)
    white_label = models.BooleanField(default=False)

    # Display & Marketing
    is_popular = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    badge_text = models.CharField(max_length=20, blank=True)
    highlight_color = models.CharField(max_length=7, default="#007BFF")

    # Status
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'price']

    def __str__(self):
        return f"{self.name} - {self.price} {self.currency}/{self.billing_cycle}"

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return round(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    @property
    def monthly_equivalent_price(self):
        """Convert price to monthly equivalent for comparison"""
        cycle_months = {
            'monthly': 1,
            'quarterly': 3,
            'semi_annual': 6,
            'annual': 12,
            'lifetime': 120,  # Assume 10 years for lifetime
        }
        return self.price / cycle_months.get(self.billing_cycle, 1)


class PlanFeature(models.Model):
    """
    Individual features that can be included in plans
    """
    FEATURE_TYPES = (
        ('limit', 'Numeric Limit'),
        ('boolean', 'Yes/No Feature'),
        ('text', 'Text Feature'),
    )

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    feature_type = models.CharField(max_length=10, choices=FEATURE_TYPES)
    category = models.CharField(max_length=50, blank=True)
    is_core_feature = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'display_order', 'name']

    def __str__(self):
        return self.name


class PlanFeatureValue(models.Model):
    """
    Feature values for specific plans
    """
    plan = models.ForeignKey(TariffPlan, on_delete=models.CASCADE, related_name='feature_values')
    feature = models.ForeignKey(PlanFeature, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)
    is_unlimited = models.BooleanField(default=False)
    is_included = models.BooleanField(default=True)

    class Meta:
        unique_together = ['plan', 'feature']

    def __str__(self):
        return f"{self.plan.name} - {self.feature.name}: {self.value}"


class UserSubscription(models.Model):
    """
    User subscriptions to tariff plans
    """
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('trial', 'Trial'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('suspended', 'Suspended'),
        ('pending', 'Pending Payment'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(TariffPlan, on_delete=models.PROTECT)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')

    # Dates
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    trial_end_date = models.DateTimeField(blank=True, null=True)
    next_billing_date = models.DateTimeField(blank=True, null=True)

    # Pricing (store at time of subscription)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    billing_cycle = models.CharField(max_length=15)

    # Auto-renewal
    auto_renew = models.BooleanField(default=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    cancellation_reason = models.TextField(blank=True)

    # Usage tracking
    properties_used = models.PositiveIntegerField(default=0)
    photos_used = models.PositiveIntegerField(default=0)
    videos_used = models.PositiveIntegerField(default=0)
    api_calls_used = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.plan.name} ({self.status})"

    @property
    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return self.status in ['active', 'trial'] and self.end_date > now

    @property
    def days_remaining(self):
        from django.utils import timezone
        if self.end_date:
            delta = self.end_date - timezone.now()
            return max(0, delta.days)
        return 0


class SubscriptionUsage(models.Model):
    """
    Track usage against subscription limits
    """
    USAGE_TYPES = (
        ('property_created', 'Property Created'),
        ('photo_uploaded', 'Photo Uploaded'),
        ('video_uploaded', 'Video Uploaded'),
        ('api_call', 'API Call'),
        ('email_sent', 'Email Sent'),
        ('sms_sent', 'SMS Sent'),
    )

    subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE, related_name='usage_logs')
    usage_type = models.CharField(max_length=20, choices=USAGE_TYPES)
    quantity = models.PositiveIntegerField(default=1)
    description = models.CharField(max_length=200, blank=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subscription.user.email} - {self.usage_type}: {self.quantity}"


class PlanUpgrade(models.Model):
    """
    Track plan upgrades and downgrades
    """
    CHANGE_TYPES = (
        ('upgrade', 'Upgrade'),
        ('downgrade', 'Downgrade'),
        ('change', 'Plan Change'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plan_changes')
    from_plan = models.ForeignKey(
        TariffPlan,
        on_delete=models.PROTECT,
        related_name='upgrades_from'
    )
    to_plan = models.ForeignKey(
        TariffPlan,
        on_delete=models.PROTECT,
        related_name='upgrades_to'
    )
    change_type = models.CharField(max_length=10, choices=CHANGE_TYPES)

    # Financial details
    proration_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    additional_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Timing
    effective_date = models.DateTimeField()
    requested_at = models.DateTimeField(auto_now_add=True)

    reason = models.TextField(blank=True)

    class Meta:
        ordering = ['-requested_at']

    def __str__(self):
        return f"{self.user.email}: {self.from_plan.name} → {self.to_plan.name}"
