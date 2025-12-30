from django.db import models

# Create your models here.
class Review(models.Model):
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