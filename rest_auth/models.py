from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db import models
from rest_auth.managers import UserManager



class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11, unique=True, default=0)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=False)
    is_email_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name_plural = "Users"