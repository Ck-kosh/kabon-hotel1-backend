from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import (
    ServiceCategory, HotelService, Gallery, Facility,
    Accommodation, Restaurant, EventFacility, ContactInformation,
    HomePageContent, ActivityLog
)
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    ServiceCategorySerializer, HotelServiceSerializer, GallerySerializer,
    FacilitySerializer, AccommodationSerializer, RestaurantSerializer,
    EventFacilitySerializer, ContactInformationSerializer,
    HomePageContentSerializer, ActivityLogSerializer, DashboardStatsSerializer
)
from .permissions import IsAdminUser, IsClientOrAdmin

User = get_user_model()


# ==================== AUTHENTICATION VIEWS ====================

class RegisterView(APIView):
    """User registration endpoint."""
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserRegistrationSerializer,
        responses={201: UserSerializer},
        description="Register a new user account."
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Registration successful!'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    """User login endpoint returning JWT tokens."""
    pass


class LogoutView(APIView):
    """User logout endpoint - blacklists the refresh token."""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Logout user by blacklisting the refresh token."
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    """Get current authenticated user information."""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: UserSerializer},
        description="Get current user details."
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve and update user profile."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user



class HomePageContentListView(generics.ListAPIView):
    """List all active homepage content sections."""
    queryset = HomePageContent.objects.filter(is_active=True)
    serializer_class = HomePageContentSerializer
    permission_classes = [AllowAny]


class ContactInformationListView(generics.ListAPIView):
    """List primary contact information."""
    queryset = ContactInformation.objects.filter(is_primary=True)
    serializer_class = ContactInformationSerializer
    permission_classes = [AllowAny]


# PROTECTED VIEWS (Auth Required)

class ServiceCategoryListView(generics.ListAPIView):
    """List all active service categories."""
    queryset = ServiceCategory.objects.filter(is_active=True)
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsClientOrAdmin]


class ServiceCategoryDetailView(generics.RetrieveAPIView):
    """Retrieve a specific service category."""
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsClientOrAdmin]


class HotelServiceListView(generics.ListAPIView):
    """List all published hotel services with search and filtering."""
    serializer_class = HotelServiceSerializer
    permission_classes = [IsClientOrAdmin]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_fields = ['category', 'featured']

    def get_queryset(self):
        queryset = HotelService.objects.filter(is_published=True).select_related('category')
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__id=category)
        return queryset


class HotelServiceDetailView(generics.RetrieveAPIView):
    """Retrieve a specific hotel service."""
    queryset = HotelService.objects.filter(is_published=True)
    serializer_class = HotelServiceSerializer
    permission_classes = [IsClientOrAdmin]


class GalleryListView(generics.ListAPIView):
    """List gallery images with filtering by category."""
    serializer_class = GallerySerializer
    permission_classes = [IsClientOrAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = Gallery.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset


class GalleryDetailView(generics.RetrieveAPIView):
    """Retrieve a specific gallery image."""
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [IsClientOrAdmin]


class FacilityListView(generics.ListAPIView):
    """List all available facilities."""
    queryset = Facility.objects.filter(is_available=True)
    serializer_class = FacilitySerializer
    permission_classes = [IsClientOrAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class FacilityDetailView(generics.RetrieveAPIView):
    """Retrieve a specific facility."""
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [IsClientOrAdmin]


class AccommodationListView(generics.ListAPIView):
    """List all available accommodations."""
    queryset = Accommodation.objects.filter(is_available=True)
    serializer_class = AccommodationSerializer
    permission_classes = [IsClientOrAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class AccommodationDetailView(generics.RetrieveAPIView):
    """Retrieve a specific accommodation."""
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    permission_classes = [IsClientOrAdmin]


class RestaurantListView(generics.ListAPIView):
    """List all active restaurants."""
    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = RestaurantSerializer
    permission_classes = [IsClientOrAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'cuisine', 'description']


class RestaurantDetailView(generics.RetrieveAPIView):
    """Retrieve a specific restaurant."""
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsClientOrAdmin]


class EventFacilityListView(generics.ListAPIView):
    """List all available event facilities."""
    queryset = EventFacility.objects.filter(is_available=True)
    serializer_class = EventFacilitySerializer
    permission_classes = [IsClientOrAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class EventFacilityDetailView(generics.RetrieveAPIView):
    """Retrieve a specific event facility."""
    queryset = EventFacility.objects.all()
    serializer_class = EventFacilitySerializer
    permission_classes = [IsClientOrAdmin]


# ==================== ADMIN VIEWS ====================

class DashboardStatsView(APIView):
    """Admin dashboard statistics."""
    permission_classes = [IsAdminUser]

    @extend_schema(
        responses={200: DashboardStatsSerializer},
        description="Get admin dashboard statistics."
    )
    def get(self, request):
        stats = {
            'total_users': User.objects.filter(is_active_user=True).count(),
            'total_services': HotelService.objects.count(),
            'total_gallery': Gallery.objects.count(),
            'total_facilities': Facility.objects.count(),
            'total_accommodations': Accommodation.objects.count(),
            'total_restaurants': Restaurant.objects.count(),
            'total_event_facilities': EventFacility.objects.count(),
            'recent_activities': ActivityLog.objects.select_related('user')[:10]
        }
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)


class UserListAdminView(generics.ListAPIView):
    """Admin: List all users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    filterset_fields = ['role', 'is_active_user']


class UserDetailAdminView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Retrieve, update or delete a user."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class ServiceCategoryAdminViewSet(generics.ListCreateAPIView):
    """Admin: List and create service categories."""
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsAdminUser]


class ServiceCategoryAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Retrieve, update or delete a service category."""
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsAdminUser]


class HotelServiceAdminViewSet(generics.ListCreateAPIView):
    """Admin: List and create hotel services."""
    queryset = HotelService.objects.all()
    serializer_class = HotelServiceSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']


class HotelServiceAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Retrieve, update or delete a hotel service."""
    queryset = HotelService.objects.all()
    serializer_class = HotelServiceSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class GalleryAdminViewSet(generics.ListCreateAPIView):
    """Admin: List and create gallery images."""
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class GalleryAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Retrieve, update or delete a gallery image."""
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class FacilityAdminViewSet(generics.ListCreateAPIView):
    """Admin: List and create facilities."""
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class FacilityAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Retrieve, update or delete a facility."""
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class AccommodationAdminViewSet(generics.ListCreateAPIView):
    """Admin: List and create accommodations."""
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    permission_classes = [IsAdminUser]


class AccommodationAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Retrieve, update or delete an accommodation."""
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    permission_classes = [IsAdminUser]


class RestaurantAdminViewSet(generics.ListCreateAPIView):
    """Admin: List and create restaurants."""
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class RestaurantAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Retrieve, update or delete a restaurant."""
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class EventFacilityAdminViewSet(generics.ListCreateAPIView):
    """Admin: List and create event facilities."""
    queryset = EventFacility.objects.all()
    serializer_class = EventFacilitySerializer
    permission_classes = [IsAdminUser]


class EventFacilityAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Retrieve, update or delete an event facility."""
    queryset = EventFacility.objects.all()
    serializer_class = EventFacilitySerializer
    permission_classes = [IsAdminUser]


class ContactInformationAdminViewSet(generics.ListCreateAPIView):
    """Admin: List and create contact information."""
    queryset = ContactInformation.objects.all()
    serializer_class = ContactInformationSerializer
    permission_classes = [IsAdminUser]


class ContactInformationAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Retrieve, update or delete contact information."""
    queryset = ContactInformation.objects.all()
    serializer_class = ContactInformationSerializer
    permission_classes = [IsAdminUser]


class HomePageContentAdminViewSet(generics.ListCreateAPIView):
    """Admin: List and create homepage content."""
    queryset = HomePageContent.objects.all()
    serializer_class = HomePageContentSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class HomePageContentAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Retrieve, update or delete homepage content."""
    queryset = HomePageContent.objects.all()
    serializer_class = HomePageContentSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class ActivityLogListView(generics.ListAPIView):
    """Admin: List activity logs."""
    queryset = ActivityLog.objects.select_related('user')
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['description', 'model_name']
    filterset_fields = ['action', 'model_name']
