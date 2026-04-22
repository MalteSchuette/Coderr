from rest_framework import serializers
from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for creating and displaying reviews, enforcing one review per reviewer/business pair."""

    def validate(self, data):
        """Prevent a reviewer from submitting a second review for the same business user."""
        if self.instance is None:
            reviewer = self.context['request'].user
            business_user = data.get('business_user')
            # Check is skipped on updates (self.instance is not None) to allow editing existing reviews
            if Review.objects.filter(
                reviewer=reviewer,
                business_user=business_user
            ).exists():
                raise serializers.ValidationError(
                    "Du hast bereits eine Bewertung für diesen Business User abgegeben.")
        return data

    class Meta:
        model = Review
        fields = [
            'id', 'business_user', 'reviewer', 'rating', 'description',
            'created_at', 'updated_at'
        ]
