from django.urls import path
from .views import (
    # Auth
    RegisterView, LoginView, LogoutView, CurrentUserView, UserProfileView,
    # Public
    HomePageContentListView, ContactInformationListView,
    # Protected
    ServiceCategoryListView, ServiceCategoryDetailView,
    HotelServiceListView, HotelServiceDetailView,
    GalleryListView, GalleryDetailView,
    FacilityListView, FacilityDetailView,
    AccommodationListView, AccommodationDetailView,
    RestaurantListView, RestaurantDetailView,
    EventFacilityListView, EventFacilityDetailView,
    # Admin
    DashboardStatsView,
    UserListAdminView, UserDetailAdminView,
    ServiceCategoryAdminViewSet, ServiceCategoryAdminDetailView,
    HotelServiceAdminViewSet, HotelServiceAdminDetailView,
    GalleryAdminViewSet, GalleryAdminDetailView,
    FacilityAdminViewSet, FacilityAdminDetailView,
    AccommodationAdminViewSet, AccommodationAdminDetailView,
    RestaurantAdminViewSet, RestaurantAdminDetailView,
    EventFacilityAdminViewSet, EventFacilityAdminDetailView,
    ContactInformationAdminViewSet, ContactInformationAdminDetailView,
    HomePageContentAdminViewSet, HomePageContentAdminDetailView,
    ActivityLogListView,
)

urlpatterns = [
    # Authentication
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/token/refresh/', LoginView.as_view(), name='token_refresh'),
    path('auth/user/', CurrentUserView.as_view(), name='current_user'),
    path('auth/profile/', UserProfileView.as_view(), name='user_profile'),

    # Public
    path('home/', HomePageContentListView.as_view(), name='home_content'),
    path('contact/', ContactInformationListView.as_view(), name='contact_info'),

    # Protected - Categories & Services
    path('categories/', ServiceCategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', ServiceCategoryDetailView.as_view(), name='category_detail'),
    path('services/', HotelServiceListView.as_view(), name='service_list'),
    path('services/<int:pk>/', HotelServiceDetailView.as_view(), name='service_detail'),

    # Protected - Gallery
    path('gallery/', GalleryListView.as_view(), name='gallery_list'),
    path('gallery/<int:pk>/', GalleryDetailView.as_view(), name='gallery_detail'),

    # Protected - Facilities
    path('facilities/', FacilityListView.as_view(), name='facility_list'),
    path('facilities/<int:pk>/', FacilityDetailView.as_view(), name='facility_detail'),

    # Protected - Accommodation
    path('accommodation/', AccommodationListView.as_view(), name='accommodation_list'),
    path('accommodation/<int:pk>/', AccommodationDetailView.as_view(), name='accommodation_detail'),

    # Protected - Restaurant
    path('restaurant/', RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurant/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant_detail'),

    # Protected - Events
    path('events/', EventFacilityListView.as_view(), name='event_list'),
    path('events/<int:pk>/', EventFacilityDetailView.as_view(), name='event_detail'),

    # Admin - Dashboard
    path('admin/dashboard/', DashboardStatsView.as_view(), name='dashboard_stats'),

    # Admin - Users
    path('admin/users/', UserListAdminView.as_view(), name='admin_user_list'),
    path('admin/users/<int:pk>/', UserDetailAdminView.as_view(), name='admin_user_detail'),

    # Admin - Categories
    path('admin/categories/', ServiceCategoryAdminViewSet.as_view(), name='admin_category_list'),
    path('admin/categories/<int:pk>/', ServiceCategoryAdminDetailView.as_view(), name='admin_category_detail'),

    # Admin - Services
    path('admin/services/', HotelServiceAdminViewSet.as_view(), name='admin_service_list'),
    path('admin/services/<int:pk>/', HotelServiceAdminDetailView.as_view(), name='admin_service_detail'),

    # Admin - Gallery
    path('admin/gallery/', GalleryAdminViewSet.as_view(), name='admin_gallery_list'),
    path('admin/gallery/<int:pk>/', GalleryAdminDetailView.as_view(), name='admin_gallery_detail'),

    # Admin - Facilities
    path('admin/facilities/', FacilityAdminViewSet.as_view(), name='admin_facility_list'),
    path('admin/facilities/<int:pk>/', FacilityAdminDetailView.as_view(), name='admin_facility_detail'),

    # Admin - Accommodation
    path('admin/accommodation/', AccommodationAdminViewSet.as_view(), name='admin_accommodation_list'),
    path('admin/accommodation/<int:pk>/', AccommodationAdminDetailView.as_view(), name='admin_accommodation_detail'),

    # Admin - Restaurant
    path('admin/restaurant/', RestaurantAdminViewSet.as_view(), name='admin_restaurant_list'),
    path('admin/restaurant/<int:pk>/', RestaurantAdminDetailView.as_view(), name='admin_restaurant_detail'),

    # Admin - Events
    path('admin/events/', EventFacilityAdminViewSet.as_view(), name='admin_event_list'),
    path('admin/events/<int:pk>/', EventFacilityAdminDetailView.as_view(), name='admin_event_detail'),

    # Admin - Contact
    path('admin/contact/', ContactInformationAdminViewSet.as_view(), name='admin_contact_list'),
    path('admin/contact/<int:pk>/', ContactInformationAdminDetailView.as_view(), name='admin_contact_detail'),

    # Admin - Homepage
    path('admin/homepage/', HomePageContentAdminViewSet.as_view(), name='admin_homepage_list'),
    path('admin/homepage/<int:pk>/', HomePageContentAdminDetailView.as_view(), name='admin_homepage_detail'),

    # Admin - Activity Logs
    path('admin/activity-logs/', ActivityLogListView.as_view(), name='admin_activity_logs'),
]
