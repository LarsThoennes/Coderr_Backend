from django.contrib import admin
from .models import Profile
class ProfileDetail(admin.ModelAdmin):
    list_display = ("user_id","user_username", "first_name", "last_name")

    def user_id(self, obj):
        return obj.user.id

    def user_username(self, obj):
        return obj.user.username

    user_username.short_description = "Username"

admin.site.register(Profile, ProfileDetail)