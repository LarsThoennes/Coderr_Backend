from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,   
        related_name="profile"
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    location = models.CharField(max_length=50, blank=True)
    tel = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
