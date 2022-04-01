from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from hashid_field import HashidField
from rest_auth.managers import UserManager


HASH_FIELD_SALT = "xj-mnplwwfxqg%3deo&worodl4h2$z5izs!(lxh*&bp%ch_"


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11, unique=True, default=0)
    email = models.EmailField(db_index=True, unique=True)
    otp_code = HashidField(
        salt=HASH_FIELD_SALT, min_length=6, unique=True, blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    is_email_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstname", "lastname", "phone_number", "username"]

    """Set User objeccts manager to UserManager"""
    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Users"
