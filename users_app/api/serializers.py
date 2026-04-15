from rest_framework import serializers
from ..models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)
    token = serializers.SerializerMethodField()
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.CharField(source='profile_type', required=True)


    def get_token(self, obj):
        from rest_framework.authtoken.models import Token
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key

    def validate(self, data):
        if data['password'] != data.pop('repeated_password'):
            raise serializers.ValidationError("Passwörter stimmen nicht überein!")
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    class Meta:
        model = CustomUser
        fields = ['token', 'username', 'email', 'user_id', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_type': {'write_only': False}
        }


class ProfileSerializer(serializers.ModelSerializer):


    type = serializers.CharField(source='profile_type', read_only=True)
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']