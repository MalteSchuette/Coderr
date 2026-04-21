from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics, permissions
from ..models import Offer, OfferDetail
from .serializers import (
    OfferCreateSerializer,
    OfferDetailSerializer,
    OfferListSerializer,
    OfferRetrieveSerializer
)
from .permissions import IsBusinessUser, IsOwnerOrReadOnly
from .filters import OfferFilter
from .pagination import OfferPagination


class OfferListCreateView(generics.ListCreateAPIView):
    
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at']

    def get_queryset(self):
        return Offer.objects.prefetch_related(
            'offer_details'
        ).annotate(
            annotated_min_price=Min('offer_details__price'),
            annotated_min_delivery=Min('offer_details__delivery_time_in_days')
        ).order_by('-created_at')

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
    queryset = Offer.objects.prefetch_related('offer_details').all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OfferRetrieveSerializer
        return OfferCreateSerializer


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
