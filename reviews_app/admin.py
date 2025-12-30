from django.contrib import admin
from .models import Review

class ReviewExtension(admin.ModelAdmin):
    list_display = ("id", "business_user", "reviewer", "rating", "description", "created_at", "updated_at")
    
admin.site.register(Review, ReviewExtension)