from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, ServiceCategory, HotelService, Gallery, Facility,
    Accommodation, Restaurant, EventFacility, ContactInformation,
    HomePageContent, ActivityLog
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active_user', 'date_joined']
    list_filter = ['role', 'is_active_user', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'address', 'avatar', 'is_active_user')}),
    )


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'display_order', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    ordering = ['display_order', 'name']


@admin.register(HotelService)
class HotelServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'is_published', 'featured', 'created_at']
    list_filter = ['is_published', 'featured', 'category', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_published', 'featured']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'display_order', 'uploaded_at']
    list_filter = ['category', 'is_featured']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'display_order']


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_available', 'opening_hours', 'created_at']
    list_filter = ['is_available']
    search_fields = ['name', 'description']


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_type', 'max_guests', 'price_per_night', 'is_available', 'featured']
    list_filter = ['room_type', 'is_available', 'featured']
    search_fields = ['name', 'description']
    list_editable = ['is_available', 'featured']


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'dining_type', 'cuisine', 'opening_hours', 'is_active']
    list_filter = ['dining_type', 'is_active']
    search_fields = ['name', 'cuisine', 'description']


@admin.register(EventFacility)
class EventFacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'facility_type', 'capacity', 'hourly_rate', 'is_available']
    list_filter = ['facility_type', 'is_available']
    search_fields = ['name', 'description']


@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ['hotel_name', 'phone', 'email', 'is_primary']
    list_filter = ['is_primary']


@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ['section', 'title', 'is_active', 'display_order']
    list_filter = ['section', 'is_active']
    list_editable = ['is_active', 'display_order']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'description', 'created_at']
    list_filter = ['action', 'model_name', 'created_at']
    search_fields = ['description', 'model_name']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'description', 'ip_address', 'created_at']
