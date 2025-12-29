from django.conf import settings
from django.db import models


class Offer(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="offers"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="offers/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    OFFER_TYPES = (
        ("basic", "Basic"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    )

    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="details"
    )

    title = models.CharField(max_length=255)
    offer_type = models.CharField(
        max_length=20,
        choices=OFFER_TYPES
    )
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.offer.title} - {self.offer_type}"

class OfferFeature(models.Model):
    detail = models.ForeignKey(
        OfferDetail,
        on_delete=models.CASCADE,
        related_name="features"
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
