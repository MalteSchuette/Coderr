from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

OFFER_TYPE_CHOICES = [
    ('basic', 'Basic'),
    ('standard', 'Standard'),
    ('premium', 'Premium')
]


class Offer(models.Model):
    """Represents a service offer created by a business user."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    image = models.ImageField(
        upload_to='offer_pictures/', blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the offer title as string representation."""
        return self.title

    class Meta:
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'
        ordering = ['-created_at']


class OfferDetail(models.Model):
    """Represents a pricing tier (basic/standard/premium) for an Offer."""

    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name='offer_details')
    title = models.CharField(max_length=40)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES)

    def __str__(self):
        """Return the detail title as string representation."""
        return self.title

    class Meta:
        verbose_name = 'Offer Detail'
        verbose_name_plural = 'Offer Details'
        ordering = ['offer_type']
