from django.db import models
from django.contrib.auth.models import AbstractUser

TYPE_CHOICES = [
    ('customer', 'Customer'),
    ('business', 'Business'),
]


class CustomUser(AbstractUser):
    """Extended user model that adds profile type and additional contact/profile fields."""

    profile_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, blank=True)
    file = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=30, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=30, blank=True)

    def __str__(self):
        """Return the username as string representation."""
        return self.username

    class Meta(AbstractUser.Meta):
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']
