from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

TYPE_CHOICES = [
    ('customer', 'Customer'),
    ('business', 'Business'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True) 
    last_name = models.CharField(max_length=30, blank=True)
    file = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=30, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=30,blank=True)
    profile_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

