from django.conf import settings
from django.db import models

class Profile(models.Model):
    """
    Model representing a user's profile.

    Each profile is linked one-to-one with a user (either customer or business).
    Contains additional information such as personal details, contact info, 
    uploaded files, description, working hours, and location. 

    Fields:
        user (OneToOneField): Link to the User model, primary key for the profile.
        first_name (CharField): User's first name (optional).
        last_name (CharField): User's last name (optional).
        file (FileField): Optional uploaded file, e.g., profile picture.
        location (CharField): User's location or address (optional).
        tel (CharField): Contact telephone number (optional).
        description (TextField): Short description or bio (optional).
        working_hours (CharField): Business or personal working hours (optional).
        created_at (DateTimeField): Timestamp of when the profile was created.
    """
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
