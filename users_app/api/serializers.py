from rest_framework import serializers
from rest_framework.authtoken.models import Token

from ..models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration; includes token in the response and validates password confirmation."""

    user_id = serializers.IntegerField(source='id', read_only=True)
    token = serializers.SerializerMethodField()
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.CharField(source='profile_type', required=True)

    def get_token(self, obj):
        """Retrieve or create an auth token for the user and return its key."""
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key

    def validate(self, data):
        """Ensure password and repeated_password match before proceeding."""
        if data['password'] != data.pop('repeated_password'):
            raise serializers.ValidationError(
                "Passwörter stimmen nicht überein!")
        return data

    def create(self, validated_data):
        """Create a new user with a hashed password via create_user."""
        user = CustomUser.objects.create_user(**validated_data)
        return user

    class Meta:
        model = CustomUser
        fields = ['token', 'username', 'email', 'user_id',
                  'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_type': {'write_only': False}
        }


class ProfileSerializer(serializers.ModelSerializer):
    """Full profile serializer used for retrieving and updating a single user profile."""

    user = serializers.IntegerField(source='id', read_only=True)
    type = serializers.CharField(source='profile_type', read_only=True)
    created_at = serializers.DateTimeField(
        source='date_joined', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location',
                  'tel', 'description', 'working_hours', 'type', 'email', 'created_at']


class ProfileListSerializer(serializers.ModelSerializer):
    """Lightweight profile serializer for listing business users."""

    user = serializers.IntegerField(source='id', read_only=True)
    type = serializers.CharField(source='profile_type', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['user', 'username', 'first_name', 'last_name', 'file',
                  'location', 'tel', 'description', 'working_hours', 'type']


class CustomerProfileListSerializer(serializers.ModelSerializer):
    """Lightweight profile serializer for listing customer users."""

    user = serializers.IntegerField(source='id', read_only=True)
    type = serializers.CharField(source='profile_type', read_only=True)
    uploaded_at = serializers.DateTimeField(
        source='date_joined', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['user', 'username', 'first_name',
                  'last_name', 'file', 'uploaded_at', 'type']