from django.db import models

class Review(models.Model):
    """
    Model representing a review written by a customer for a business user.

    Each review is linked to the business being reviewed and the customer 
    who wrote the review. Contains a numerical rating, a textual description, 
    and timestamps for creation and updates.

    Fields:
        business_user (ForeignKey): Reference to the business user being reviewed.
        reviewer (ForeignKey): Reference to the customer user who wrote the review.
        rating (IntegerField): Numeric rating given by the reviewer.
        description (TextField): Optional textual feedback from the reviewer.
        created_at (DateTimeField): Timestamp when the review was created.
        updated_at (DateTimeField): Timestamp when the review was last updated.
    """

    business_user = models.ForeignKey(
        'auth_app.User',
        on_delete=models.CASCADE,
        related_name='business_user'
    )
    reviewer = models.ForeignKey(
        'auth_app.User',
        on_delete=models.CASCADE,
        related_name='reviewer'
    )
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)