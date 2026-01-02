from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    This model adds a `type` field to distinguish between different user roles
    on the platform.

    User types:
    - customer: Can browse offers, create orders and write reviews
    - business: Can create offers and manage incoming orders
    """
    USER_TYPES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
    )

    type = models.CharField(
        max_length=20,
        choices=USER_TYPES
    )
