from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username
