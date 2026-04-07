from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

OFFER_TYPE_CHOICES = [
    ('basic', 'Basic'),
    ('standard', 'Standard'),
    ('premium', 'Premium'),
]

# Create your models here.
class Order(models.Model):
    offer_detail = models.ForeignKey('offers_app.OfferDetail', on_delete=models.SET_NULL, null=True)
    customer_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='customer_orders')
    business_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='business_orders')
    title = models.CharField(max_length=40)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

