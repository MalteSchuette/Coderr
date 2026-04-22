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
    """List all offers with filtering/search/ordering, or create a new offer (business users only)."""

    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at']

    def get_queryset(self):
        """Return offers with prefetched details and annotated aggregate price/delivery fields."""
        # Annotations are required by OfferFilter for price and delivery time filtering
        return Offer.objects.prefetch_related(
            'offer_details'
        ).annotate(
            annotated_min_price=Min('offer_details__price'),
            annotated_min_delivery=Min('offer_details__delivery_time_in_days')
        ).order_by('-created_at')

    def get_permissions(self):
        """Require authentication and a business profile for POST; allow anyone to list."""
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        """Use the create serializer for POST requests and the list serializer for GET."""
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferListSerializer

    def perform_create(self, serializer):
        """Attach the authenticated user as the offer owner before saving."""
        serializer.save(user=self.request.user)


class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single offer; write access is restricted to the owner."""

    queryset = Offer.objects.prefetch_related('offer_details').all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        """Use the retrieve serializer for GET requests and the create serializer for mutations."""
        if self.request.method == 'GET':
            return OfferRetrieveSerializer
        return OfferCreateSerializer


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    """Retrieve a single OfferDetail by its primary key."""

    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
