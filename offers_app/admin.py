from django.contrib import admin
from .models import Offer, OfferDetail, OfferFeature

class OfferExtension(admin.ModelAdmin):
    list_display = ("id", "title", "owner_id", "description")

class OfferDetailExtension(admin.ModelAdmin):
    list_display = ("id", "offer", "title", "price", "delivery_time_in_days")

class OfferFeatureExtension(admin.ModelAdmin):
    list_display = ("id", "detail", "name")
    
admin.site.register(Offer, OfferExtension)
admin.site.register(OfferDetail, OfferDetailExtension)
admin.site.register(OfferFeature, OfferFeatureExtension)