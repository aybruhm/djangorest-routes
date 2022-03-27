from rest_framework.test import APITestCase
from rest_framework import status


class AuthOniichanTestCase(APITestCase):
    """
    The test_post method tests the post request to the register endpoint.
    The test_bad_request method tests the post request to the register endpoint with missing fields
    """
    
    def test_user_register(self):
        data = {
            "firstname": "israel", "lastname": "abraham",
            "username": "abram", "password": "somereallystrongpassword",
            "phone_number": "08137281916", "email": "abram@test.com"
        }
        response = self.client.post("http://127.0.0.1:8000/rest_auth/register/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_register_bad_request(self):
        data = {
            "username": "abram", "password": "somereallystrongpassword",
            "phone_number": "08137281916", "email": "abram@test.com"
        }
        response = self.client.post("http://127.0.0.1:8000/rest_auth/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class ConfirmOniichanOTPTestCase(APITestCase):
    
    def test_confirm_otp_bad_request(self):
        data = {
            "email": "abram@test.com", 
            "otp_code": "453521"
        }
        response = self.client.post("http://127.0.0.1:8000/rest_auth/confirm_otp/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    