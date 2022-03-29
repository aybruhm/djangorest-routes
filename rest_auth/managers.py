# from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
        self,
        firstname: str,
        lastname: str,
        email: str,
        phone_number: str,
        password=None,
    ):
        """Creates normal user"""

        if email is None:
            raise TypeError("Users must have an email address")

        if phone_number is None:
            raise TypeError("User must have a phone number")

        user = self.create_user(
            firstname=firstname,
            lastname=lastname,
            email=self.normalize_email(email),
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(
        self,
        firstname: str,
        lastname: str,
        phone_number: str,
        email: str,
        password=None,
    ):
        """Creates super user"""

        if firstname is None:
            raise TypeError("Users must have a Firstname")

        if email is None:
            raise TypeError("Users must have an email address")

        if phone_number is None:
            raise TypeError("User must have a phone number")

        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone_number=phone_number,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user
