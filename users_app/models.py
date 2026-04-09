from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

TYPE_CHOICES = [
    ('customer', 'Customer'),
    ('business', 'Business'),
]

class CustomUser(AbstractUser):
    profile_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=30, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=30,blank=True)


    def __str__(self):
        return self.user.username

