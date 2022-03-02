from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()
User.__init__.unique = True


class UserSerializer(serializers.ModelSerializer):
    """
    A serializer that display the user information
    """

    class Meta:
        model = User
        ref_name = "Auth User"
        fields = [
            "id", "firstname", "lastname", "email"
        ]
        extra_kwargs = {
            "email": {
                "read_only": True
            }
        }


class AuthUserSerializer(serializers.ModelSerializer):
    """
    A serializer for registering the user
    """

    class Meta:
        model = User
        ref_name = "Auth User"
        fields = [
            "id", "firstname", "lastname", "email",
            "password", "phone_number"
        ]
        extra_kwargs = {
            "password": {
                "write_only": True
            },
            "email": {
                "write_only": True
            }
        }


class UserLoginSerializer(serializers.Serializer):
    """
    A user serializer for logging in the user
    """
    email = serializers.EmailField(max_length=300, required=True)
    password = serializers.CharField(required=True)
    

class ChangeUserPasswordSerializer(serializers.Serializer):
    """
    Change current user password
    """
    email = serializers.EmailField(required=True)
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    repeat_new_password = serializers.CharField(required=True)


class OTPSerializer(serializers.Serializer):
    """
    Serializer to validate the otp code and user via email
    """
    email = serializers.EmailField(max_length=255, required=True)
    otp_code = serializers.CharField(required=True, max_length=6)


class ResendOTPSerializer(serializers.Serializer):
    """
    Serializer to resend OTP code to user's email
    """
    email = serializers.EmailField(max_length=255, required=True)


class EmptySerializer(serializers.Serializer):
    pass


class SuspendUserSerializer(serializers.Serializer):
    """
    Serializer to suspend a user
    """
    username = serializers.CharField(max_length=255, required=True)
    is_active = serializers.BooleanField(required=True)