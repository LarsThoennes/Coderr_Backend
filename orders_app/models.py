from django.db import models
class Order(models.Model):
    """
    Represents a placed order on the platform.

    An order is created by a customer user based on an OfferDetail
    and is fulfilled by a business user. It stores a snapshot of
    the offer data at the time of ordering.
    """

    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    customer_user = models.ForeignKey(
        'auth_app.User',
        on_delete=models.CASCADE,
        related_name='customer_orders'
    )
    business_user = models.ForeignKey(
        'auth_app.User',
        on_delete=models.CASCADE,
        related_name='business_orders'
    )
    title = models.CharField(max_length=100)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderFeature(models.Model):
    """
    Represents a single feature included in an order.

    Features are copied from the related OfferDetail at the time
    the order is created to keep historical consistency.
    """
    features = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_features'
    )
    name = models.CharField(max_length=255)