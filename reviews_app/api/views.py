from rest_framework import generics, permissions

from .permissions import IsCustomerUser, IsReviewerOrReadOnly
from ..models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    """List all reviews or create a new review (customer users only)."""

    queryset = Review.objects.select_related(
        'business_user', 'reviewer'
    ).all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        """Require customer profile for POST; any authenticated user may list reviews."""
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsCustomerUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """Attach the authenticated user as the reviewer before saving."""
        serializer.save(reviewer=self.request.user)


class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single review; write access is restricted to the reviewer."""

    queryset = Review.objects.select_related(
        'business_user', 'reviewer'
    ).all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewerOrReadOnly]
