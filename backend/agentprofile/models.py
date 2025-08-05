from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

User = get_user_model()


class AgentProfile(models.Model):
    """
    Extended profile for real estate agents
    """
    EXPERIENCE_CHOICES = (
        ('0-1', '0-1 years'),
        ('1-3', '1-3 years'),
        ('3-5', '3-5 years'),
        ('5-10', '5-10 years'),
        ('10+', '10+ years'),
    )

    SPECIALIZATION_CHOICES = (
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('luxury', 'Luxury Properties'),
        ('rental', 'Rental Properties'),
        ('investment', 'Investment Properties'),
        ('land', 'Land & Development'),
    )

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='agent_profile',
        limit_choices_to={'user_type': 'agent'}
    )
    
    # Professional Information
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry = models.DateField()
    agency_name = models.CharField(max_length=100, blank=True)
    agency_address = models.TextField(blank=True)
    years_experience = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES)
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    
    # Contact & Social
    office_phone = models.CharField(max_length=17, blank=True)
    website = models.URLField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    facebook_profile = models.URLField(blank=True)
    instagram_profile = models.URLField(blank=True)
    
    # Professional Description
    bio = models.TextField(help_text="Professional biography and experience")
    languages_spoken = models.CharField(max_length=200, blank=True, help_text="Comma-separated languages")
    
    # Service Areas
    service_areas = models.ManyToManyField('locations.Area', related_name='agents', blank=True)
    
    # Professional Status
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Performance Metrics
    total_sales = models.PositiveIntegerField(default=0)
    total_rentals = models.PositiveIntegerField(default=0)
    client_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_reviews = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.agency_name}"

    class Meta:
        ordering = ['-is_featured', '-client_rating']


class AgentCertification(models.Model):
    """
    Professional certifications for agents
    """
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=100)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    certificate_number = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.agent.user.full_name} - {self.name}"


class AgentReview(models.Model):
    """
    Client reviews for agents
    """
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agent_reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=100)
    comment = models.TextField()
    is_verified = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['agent', 'reviewer']

    def __str__(self):
        return f"{self.agent.user.full_name} - {self.rating}/5 by {self.reviewer.full_name}"


class AgentAchievement(models.Model):
    """
    Awards and achievements for agents
    """
    ACHIEVEMENT_TYPES = (
        ('award', 'Award'),
        ('recognition', 'Recognition'),
        ('milestone', 'Milestone'),
        ('certification', 'Certification'),
    )

    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    achievement_type = models.CharField(max_length=15, choices=ACHIEVEMENT_TYPES)
    date_achieved = models.DateField()
    issuing_organization = models.CharField(max_length=100, blank=True)
    certificate_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_achieved']

    def __str__(self):
        return f"{self.agent.user.full_name} - {self.title}"


class AgentSchedule(models.Model):
    """
    Agent availability schedule
    """
    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name='schedule')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['agent', 'day_of_week']
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.agent.user.full_name} - {self.get_day_of_week_display()}"


class AgentContact(models.Model):
    """
    Contact inquiries sent to agents
    """
    STATUS_CHOICES = (
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    )

    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name='inquiries')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agent_contacts')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    phone_number = models.CharField(max_length=17, blank=True)
    preferred_contact_method = models.CharField(
        max_length=10,
        choices=[('email', 'Email'), ('phone', 'Phone'), ('whatsapp', 'WhatsApp')],
        default='email'
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new')
    agent_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Contact for {self.agent.user.full_name} from {self.client.full_name}"
