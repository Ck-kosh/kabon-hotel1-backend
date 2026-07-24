from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


class User(AbstractUser):
    """Extended User model with role-based access control."""

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('client', 'Registered Client'),
        ('admin', 'Administrator'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    is_active_user = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_client(self):
        return self.role == 'client'


class ServiceCategory(models.Model):
    """Categories for hotel services."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="Icon class name")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'service_categories'
        ordering = ['display_order', 'name']
        verbose_name_plural = 'Service Categories'

    def __str__(self):
        return self.name


class HotelService(models.Model):
    """Hotel services and amenities."""

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='services'
    )
    image = models.ImageField(
        upload_to='services/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., '1 hour', 'Full day'")
    is_published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hotel_services'
        ordering = ['-featured', '-created_at']

    def __str__(self):
        return self.title


class Gallery(models.Model):
    """Image gallery for the hotel."""

    CATEGORY_CHOICES = [
        ('interior', 'Interior'),
        ('exterior', 'Exterior'),
        ('rooms', 'Rooms'),
        ('dining', 'Dining'),
        ('events', 'Events'),
        ('facilities', 'Facilities'),
        ('spa', 'Spa & Wellness'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='gallery/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gallery'
        ordering = ['-is_featured', 'display_order', '-uploaded_at']
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return self.title


class Facility(models.Model):
    """Hotel facilities and amenities."""

    name = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(
        upload_to='facilities/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    is_available = models.BooleanField(default=True)
    opening_hours = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'facilities'
        ordering = ['name']

    def __str__(self):
        return self.name


class Accommodation(models.Model):
    """Accommodation types available at the hotel."""

    ROOM_TYPES = [
        ('standard', 'Standard Room'),
        ('deluxe', 'Deluxe Room'),
        ('suite', 'Suite'),
        ('presidential', 'Presidential Suite'),
        ('family', 'Family Room'),
        ('executive', 'Executive Room'),
    ]

    name = models.CharField(max_length=200)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='standard')
    description = models.TextField()
    amenities = models.JSONField(default=list, help_text="List of amenities")
    max_guests = models.PositiveIntegerField(default=2)
    room_size = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., '45 sqm'")
    bed_type = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 'King Size'")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ManyToManyField(Gallery, blank=True, related_name='accommodations')
    is_available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accommodations'
        ordering = ['-featured', 'price_per_night']

    def __str__(self):
        return f"{self.name} ({self.get_room_type_display()})"


class Restaurant(models.Model):
    """Restaurant and dining information."""

    DINING_TYPES = [
        ('restaurant', 'Restaurant'),
        ('cafe', 'Cafe'),
        ('bar', 'Bar'),
        ('lounge', 'Lounge'),
        ('room_service', 'Room Service'),
    ]

    name = models.CharField(max_length=200)
    dining_type = models.CharField(max_length=20, choices=DINING_TYPES, default='restaurant')
    description = models.TextField()
    cuisine = models.CharField(max_length=200, blank=True, null=True)
    menu_highlights = models.JSONField(default=list, help_text="List of highlighted menu items")
    opening_hours = models.CharField(max_length=200)
    dress_code = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(
        upload_to='restaurants/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    capacity = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'restaurants'
        ordering = ['name']

    def __str__(self):
        return self.name


class EventFacility(models.Model):
    """Events and conference facilities."""

    FACILITY_TYPES = [
        ('conference', 'Conference Room'),
        ('ballroom', 'Ballroom'),
        ('meeting', 'Meeting Room'),
        ('banquet', 'Banquet Hall'),
        ('outdoor', 'Outdoor Venue'),
    ]

    name = models.CharField(max_length=200)
    facility_type = models.CharField(max_length=20, choices=FACILITY_TYPES, default='conference')
    description = models.TextField()
    capacity = models.PositiveIntegerField()
    floor_plan = models.CharField(max_length=200, blank=True, null=True, help_text="e.g., 'Theater: 200, Classroom: 120'")
    equipment = models.JSONField(default=list, help_text="List of available equipment")
    images = models.ManyToManyField(Gallery, blank=True, related_name='event_facilities')
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'event_facilities'
        ordering = ['capacity']
        verbose_name_plural = 'Event Facilities'

    def __str__(self):
        return f"{self.name} ({self.get_facility_type_display()} - {self.capacity} pax)"


class ContactInformation(models.Model):
    """Hotel contact information."""

    hotel_name = models.CharField(max_length=200, default='Kabon Hotel')
    tagline = models.CharField(max_length=300, blank=True, null=True)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    social_media = models.JSONField(default=dict, help_text="Social media links")
    business_hours = models.JSONField(default=dict, help_text="Business hours by day")
    emergency_contact = models.CharField(max_length=50, blank=True, null=True)
    is_primary = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contact_information'
        verbose_name_plural = 'Contact Information'

    def __str__(self):
        return self.hotel_name


class HomePageContent(models.Model):
    """Homepage content management."""

    SECTION_CHOICES = [
        ('hero', 'Hero Banner'),
        ('welcome', 'Welcome Message'),
        ('about', 'About Section'),
        ('features', 'Features Section'),
        ('testimonials', 'Testimonials'),
        ('cta', 'Call to Action'),
    ]

    section = models.CharField(max_length=20, choices=SECTION_CHOICES, unique=True)
    title = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=500, blank=True, null=True)
    content = models.TextField()
    image = models.ImageField(
        upload_to='homepage/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    button_text = models.CharField(max_length=100, blank=True, null=True)
    button_link = models.CharField(max_length=200, blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'homepage_content'
        ordering = ['display_order']
        verbose_name_plural = 'Homepage Content'

    def __str__(self):
        return f"{self.get_section_display()} - {self.title[:50]}"


class ActivityLog(models.Model):
    """Activity logging for admin actions."""

    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('publish', 'Publish'),
        ('unpublish', 'Unpublish'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='activity_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'activity_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.action} {self.model_name} at {self.created_at}"
