from django.contrib import admin
from rest_routes.models import User



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "firstname", "lastname", "email", "username")
    list_filter = ("id", "email", "username")