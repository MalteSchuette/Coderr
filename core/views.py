from django.db.models import Avg
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from offers_app.models import Offer
from reviews_app.models import Review

User = get_user_model()


class BaseInfoView(APIView):
    """Return platform-wide statistics used for the public landing page."""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """Aggregate and return review count, average rating, business user count, and offer count."""
        review_count = Review.objects.count()
        # Fall back to 0 when no reviews exist to avoid returning None in the response
        average_rating = Review.objects.aggregate(
            average=Avg('rating'))['average'] or 0
        business_profile_count = User.objects.filter(
            profile_type='business').count()
        offer_count = Offer.objects.count()
        data = {
            'review_count': review_count,
            'average_rating': average_rating,
            'business_profile_count': business_profile_count,
            'offer_count': offer_count,
        }
        return Response(data)
