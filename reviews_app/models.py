from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    """Represents a rating and written review left by a customer for a business user.

    Each reviewer can leave at most one review per business user (unique_together constraint).
    """

    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews_received')
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='reviews_written')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business_user', 'reviewer')
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        """Return a human-readable representation showing reviewer and business user."""
        return f"{self.reviewer} → {self.business_user}"
