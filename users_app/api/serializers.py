from rest_framework import serializers
from ..models import CustomUser




class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        from rest_framework.authtoken.models import Token
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key

    class Meta:
        model = CustomUser
        fields = ['token', 'username', 'email', 'user_id']


class ProfileSerializer(serializers.ModelSerializer):


    type = serializers.CharField(source='profile_type', read_only=True)
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']