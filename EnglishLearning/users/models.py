from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200 , blank=True , null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    profile_img = models.ImageField(
        blank=True,
        null=True,
        upload_to="profiles_img/",
        default="profiles_img/default.jpg",
    )
    profile_channel_art = models.ImageField(
        blank=True,
        null=True,
        upload_to="profiles_channel_art/",
        default="profiles_channel_art/default.jpg",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.user.username)
