from django.contrib import admin
from rest_routes.models import User



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "username")
    list_filter = ("id", "email", "username")