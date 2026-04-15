from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from ..models import CustomUser
from .serializers import UserSerializer, ProfileSerializer


class RegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'user_id': user.id
        })
    

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer


class BusinessProfilesView(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(profile_type='business')


class CustomerProfilesView(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(profile_type='customer')


