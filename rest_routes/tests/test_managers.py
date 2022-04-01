from unittest import mock
from rest_routes import managers, models
from rest_framework.test import APITestCase


# class UserManagerTestCase(APITestCase):
#     def test_user_manager(self):
#         # user = managers.UserManager.create_user(
#         #     self, firstname="israel", lastname="abraham", email="abram@test.com",
#         #     phone_number="09035588822", password="somereallystrongpassword"
#         # )
#         # self.AssertEqual(user, models.User)

#         with mock.patch("django.contrib.auth.models.User") as user_mock:
#             user_mock.objects = mock.MagicMock()
#             user_mock.objects.create_user = mock.MagicMock()
#             user_mock.objects.create_user.return_value = models.User()

#             user_manager = models.UserManager()
#             user_manager.create_user(
#                 "israel",
#                 "abraham",
#                 "Test@test.com",
#                 "09035588822",
#                 "somereallystrongpassword",
#             )

#             self.assertTrue(user_mock.objects.create_user.called)
