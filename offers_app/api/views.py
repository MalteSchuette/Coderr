from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from ..models import Offer, OfferDetail
from .serializers import (
    OfferCreateSerializer, 
    OfferDetailSerializer, 
    OfferListSerializer, 
    OfferRetrieveSerializer
)
from .permissions import IsBusinessUser, IsOwnerOrReadOnly


class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OfferRetrieveSerializer
        return OfferCreateSerializer

    def perform_update(self, serializer):
        offer = self.get_object()
        if offer.user != self.request.user:
            raise PermissionDenied("Only the creator is allowed to edit this offer.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Only the creator is allowed to delete this offer.")
        instance.delete()


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]