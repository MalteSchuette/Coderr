from rest_framework import serializers
from ..models import Profile

class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField()
    type = serializers.CharField(source='profile_type', read_only=True)

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at',]
