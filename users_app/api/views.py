from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from .serializers import ProfileListSerializer, UserSerializer, ProfileSerializer, CustomerProfileListSerializer
from ..models import CustomUser


class RegistrationView(generics.CreateAPIView):
    """Handle new user registration; accessible without authentication."""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        """Save the new user instance after successful validation."""
        serializer.save()


class LoginView(ObtainAuthToken):
    """Authenticate a user and return a token along with basic profile information."""

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Validate credentials, retrieve or create an auth token, and return user data."""
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # get_or_create ensures idempotency; existing tokens are reused
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'user_id': user.id
        })


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve or update a user profile; write access is restricted to the profile owner."""

    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class BusinessProfilesView(generics.ListAPIView):
    """List all users with a business profile."""

    serializer_class = ProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only users whose profile type is 'business'."""
        return CustomUser.objects.filter(profile_type='business')


class CustomerProfilesView(generics.ListAPIView):
    """List all users with a customer profile."""

    serializer_class = CustomerProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only users whose profile type is 'customer'."""
        return CustomUser.objects.filter(profile_type='customer')
