import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

# User model Imports
from rest_routes.models import User


class BaseTestCase(APITestCase):
    
    def setUp(self) -> None:
        ...
    
    @property
    def bearer_token_login(self):
        ...


class RegisterUserTestCase(APITestCase):
    ...
    

class LoginUserTestCase(APITestCase):
    ...
    

class ConfirmUserOTPTestCase(APITestCase):
    ...
    

class ResendUserOTPTestCase(APITestCase):
    ...
    

class SuspendUserTestCase(APITestCase):
    ...
    

class ChangeUserPasswordTestCase(APITestCase):
    ...
    

class ResetUserPasswordOTPTestCase(APITestCase):
    ...
    

class ConfirmResetUserPasswordOTPTestCase(APITestCase):
    ...
    

class CompleteResetUserPasswordOTPTestCase(APITestCase):
    ...
    

class LogUserOutTestCase(APITestCase):
    ...
    
class AuthenticationTestCase(APITestCase):

    def test_register_user(self):
        """
        Ensure we can create a new user object.
        """
        
        url = reverse("authentication:register_user")
        data = {
            "firstname": "Israel",
            "lastname": "Abraham",
            "username": "abram",
            "password": "somereally_strongpassword_2002",
            "phone_number": "09012345654",
            "email": "abram@test.com",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "abram")
        self.assertEqual(User.objects.get().email, "abram@test.com")
        
    def test_login_user(self):
        pass
    
    def test_refresh_login_user(self):
        pass
    
    def test_confirm_user_otp(self):
        pass
    
    def test_resend_user_otp(self):
        pass
    
    def test_suspend_user(self):
        pass
    
    def test_change_user_password(self):
        pass
    
    def test_reset_user_password_otp(self):
        pass
    
    def test_confirm_user_password_otp(self):
        pass
    
    def test_reset_user_password_otp_complete(self):
        pass
    
    def test_log_user_out(self):
        pass