from rest_framework.test import APITestCase
from rest_routes.models import User



class UserTestCase(APITestCase):
    
    def test_string_representation(self):
        user = User(email="abram@test.com")
        self.assertEqual(str(user), user.email)