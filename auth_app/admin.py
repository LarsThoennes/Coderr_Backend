from django.contrib import admin
from .models import User

class UserDeatil(admin.ModelAdmin):
    list_display = ("id","username", "email", "type")
    readonly_fields = ["type"]

admin.site.register(User, UserDeatil)