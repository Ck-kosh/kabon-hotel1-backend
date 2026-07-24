from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_field
from .models import (
    ServiceCategory, HotelService, Gallery, Facility,
    Accommodation, Restaurant, EventFacility, ContactInformation,
    HomePageContent, ActivityLog
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer for profile and admin management."""
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'role', 'role_display', 'phone', 'address', 'avatar',
                  'is_active_user', 'date_joined', 'created_at']
        read_only_fields = ['id', 'date_joined', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 
                  'password', 'password_confirm', 'phone']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data['role'] = 'client'
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class ServiceCategorySerializer(serializers.ModelSerializer):
    """Serializer for service categories."""
    service_count = serializers.SerializerMethodField()

    class Meta:
        model = ServiceCategory
        fields = '__all__'

    @extend_schema_field(serializers.IntegerField())
    def get_service_count(self, obj):
        return obj.services.filter(is_published=True).count()


class HotelServiceSerializer(serializers.ModelSerializer):
    """Serializer for hotel services."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=ServiceCategory.objects.all())

    class Meta:
        model = HotelService
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    """Serializer for gallery images."""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = '__all__'

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class FacilitySerializer(serializers.ModelSerializer):
    """Serializer for hotel facilities."""

    class Meta:
        model = Facility
        fields = '__all__'


class AccommodationSerializer(serializers.ModelSerializer):
    """Serializer for accommodation types."""
    room_type_display = serializers.CharField(source='get_room_type_display', read_only=True)
    images = GallerySerializer(many=True, read_only=True)
    image_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Gallery.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = Accommodation
        fields = '__all__'

    def create(self, validated_data):
        image_ids = validated_data.pop('image_ids', [])
        accommodation = super().create(validated_data)
        accommodation.images.set(image_ids)
        return accommodation

    def update(self, instance, validated_data):
        image_ids = validated_data.pop('image_ids', None)
        accommodation = super().update(instance, validated_data)
        if image_ids is not None:
            accommodation.images.set(image_ids)
        return accommodation


class RestaurantSerializer(serializers.ModelSerializer):
    """Serializer for restaurant and dining."""
    dining_type_display = serializers.CharField(source='get_dining_type_display', read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'


class EventFacilitySerializer(serializers.ModelSerializer):
    """Serializer for event facilities."""
    facility_type_display = serializers.CharField(source='get_facility_type_display', read_only=True)
    images = GallerySerializer(many=True, read_only=True)
    image_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Gallery.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = EventFacility
        fields = '__all__'

    def create(self, validated_data):
        image_ids = validated_data.pop('image_ids', [])
        facility = super().create(validated_data)
        facility.images.set(image_ids)
        return facility

    def update(self, instance, validated_data):
        image_ids = validated_data.pop('image_ids', None)
        facility = super().update(instance, validated_data)
        if image_ids is not None:
            facility.images.set(image_ids)
        return facility


class ContactInformationSerializer(serializers.ModelSerializer):
    """Serializer for contact information."""

    class Meta:
        model = ContactInformation
        fields = '__all__'


class HomePageContentSerializer(serializers.ModelSerializer):
    """Serializer for homepage content."""
    section_display = serializers.CharField(source='get_section_display', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HomePageContent
        fields = '__all__'

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class ActivityLogSerializer(serializers.ModelSerializer):
    """Serializer for activity logs."""
    user_name = serializers.CharField(source='user.username', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = ActivityLog
        fields = '__all__'


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics."""
    total_users = serializers.IntegerField()
    total_services = serializers.IntegerField()
    total_gallery = serializers.IntegerField()
    total_facilities = serializers.IntegerField()
    total_accommodations = serializers.IntegerField()
    total_restaurants = serializers.IntegerField()
    total_event_facilities = serializers.IntegerField()
    recent_activities = ActivityLogSerializer(many=True)
