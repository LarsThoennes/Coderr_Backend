from django.contrib import admin
from .models import Order, OrderFeature

class OrderExtension(admin.ModelAdmin):
    list_display = ("id", "customer_user", "business_user", "title", "revisions", "delivery_time_in_days")

class OrderFeatureExtension(admin.ModelAdmin):
    list_display = ("id","name")
    
admin.site.register(Order, OrderExtension)
admin.site.register(OrderFeature, OrderFeatureExtension)
