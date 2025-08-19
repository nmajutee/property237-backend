from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MediaCategory(models.Model):
    """
    Categories for media files
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Media Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class MediaFile(models.Model):
    """
    Generic media file model for the API
    """
    FILE_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('virtual_tour', 'Virtual Tour'),
    )

    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to='media_files/')
    file_type = models.CharField(max_length=15, choices=FILE_TYPES, default='image')
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'uploaded_at']

    def __str__(self):
        return f"{self.property.title} - {self.title or self.file.name}"


class PropertyImage(models.Model):
    """
    Images for properties
    """
    IMAGE_TYPES = (
        ('exterior', 'Exterior'),
        ('interior', 'Interior'),
        ('bedroom', 'Bedroom'),
        ('bathroom', 'Bathroom'),
        ('kitchen', 'Kitchen'),
        ('living_room', 'Living Room'),
        ('balcony', 'Balcony'),
        ('garden', 'Garden'),
        ('parking', 'Parking'),
        ('amenities', 'Amenities'),
        ('floor_plan', 'Floor Plan'),
        ('other', 'Other'),
    )

    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    image_type = models.CharField(max_length=15, choices=IMAGE_TYPES, default='other')
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.property.title} - {self.get_image_type_display()}"

    def save(self, *args, **kwargs):
        # Ensure only one primary image per property
        if self.is_primary:
            PropertyImage.objects.filter(
                property=self.property,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)


class PropertyVideo(models.Model):
    """
    Videos for properties
    """
    VIDEO_TYPES = (
        ('tour', 'Property Tour'),
        ('walkthrough', 'Walkthrough'),
        ('drone', 'Drone View'),
        ('neighborhood', 'Neighborhood'),
        ('testimonial', 'Testimonial'),
        ('other', 'Other'),
    )

    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to='property_videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="YouTube, Vimeo, or other video URL")
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    video_type = models.CharField(max_length=15, choices=VIDEO_TYPES, default='tour')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration = models.DurationField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)  # Fixed: was BooleanFilter
    order = models.PositiveIntegerField(default=0)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.property.title} - {self.title}"


class PropertyDocument(models.Model):
    """
    Documents related to properties
    """
    DOCUMENT_TYPES = (
        ('floor_plan', 'Floor Plan'),
        ('title_deed', 'Title Deed'),
        ('noc', 'No Objection Certificate'),
        ('approval', 'Approval Document'),
        ('tax_receipt', 'Tax Receipt'),
        ('utility_bill', 'Utility Bill'),
        ('lease_agreement', 'Lease Agreement'),
        ('inspection_report', 'Inspection Report'),
        ('valuation', 'Property Valuation'),
        ('brochure', 'Property Brochure'),
        ('other', 'Other'),
    )

    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='property_documents/')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)  # in bytes
    is_public = models.BooleanField(default=False)
    requires_authentication = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['document_type', 'created_at']

    def __str__(self):
        return f"{self.property.title} - {self.title}"


class VirtualTour(models.Model):
    """
    360° virtual tours for properties
    """
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='virtual_tours')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    tour_url = models.URLField(help_text="URL to 360° tour (Matterport, etc.)")
    embed_code = models.TextField(blank=True, help_text="HTML embed code for the tour")
    thumbnail = models.ImageField(upload_to='tour_thumbnails/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.property.title} - {self.title}"


class MediaGallery(models.Model):
    """
    Organized galleries of property media
    """
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='galleries')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(MediaCategory, on_delete=models.SET_NULL, null=True, blank=True)
    images = models.ManyToManyField(PropertyImage, through='GalleryImage', blank=True)
    videos = models.ManyToManyField(PropertyVideo, blank=True)
    is_public = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Media Galleries"
        ordering = ['name']

    def __str__(self):
        return f"{self.property.title} - {self.name}"


class GalleryImage(models.Model):
    """
    Through model for Gallery-Image relationship with ordering
    """
    gallery = models.ForeignKey(MediaGallery, on_delete=models.CASCADE)
    image = models.ForeignKey(PropertyImage, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        unique_together = ['gallery', 'image']

    def __str__(self):
        return f"{self.gallery.name} - {self.image.title}"


class MediaTag(models.Model):
    """
    Tags for media organization
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#000000")  # Hex color
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ImageTag(models.Model):
    """
    Many-to-many relationship between images and tags
    """
    image = models.ForeignKey(PropertyImage, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(MediaTag, on_delete=models.CASCADE, related_name='images')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['image', 'tag']

    def __str__(self):
        return f"{self.image.title} - {self.tag.name}"