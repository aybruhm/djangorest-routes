"""Django Imports"""
from django.contrib.auth import get_user_model


"""Rest Framework Imports"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


"""Third Party Imports"""
from rest_api_payload import success_response


"""Custom app -> Rest Auth Imports"""
from rest_routes.otp_verifications import OTPVerification


"""Class Instantiations"""
otp_verify = OTPVerification()
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer that displays a user information"""

    class Meta:
        model = User
        fields = ["id", "firstname", "lastname", "email", "username"]
        extra_kwargs = {"email": {"read_only": True}}


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for registering a user"""

    class Meta:
        model = User
        fields = (
            "firstname",
            "lastname",
            "username",
            "email",
            "password",
            "phone_number",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"write_only": True},
        }

    def create(self, validated_data):
        """
        Create a new user

        :param validated_data: The data that was sent to the server
        :return: The user object.
        """
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()

        """Send otp code to user's email address"""
        otp_sent = otp_verify.send_otp_code_to_email(
            email=user.email, first_name=user.firstname
        )

        if otp_sent:
            return user


class UserLoginObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        """The default result (access/refresh tokens)"""
        data = super(UserLoginObtainPairSerializer, self).validate(attrs)

        """Custom data you want to include"""
        data.update({"email": self.user.email})
        data.update({"firstname": self.user.firstname})
        data.update({"lastname": self.user.lastname})
        data.update({"id": self.user.id})

        """Return custom data in the response"""
        payload = success_response(
            status="success", message="Login successful", data=data
        )
        return payload


class ChangeUserPasswordSerializer(serializers.Serializer):
    """Serializer to change user password"""

    email = serializers.EmailField(required=True)
    current_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Current Password"},
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "New Password"},
    )
    repeat_new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Repeat New Password"},
    )


class ResetPasswordOTPSerializer(serializers.Serializer):
    """Serializer to reset password using OTP"""

    email = serializers.EmailField(max_length=255, required=True)


class CompleteResetPasswordOTPSerializer(serializers.Serializer):
    """Serializer to change password after OTP validation for reset password"""

    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(
        max_length=255,
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Password"},
    )
    confirm_password = serializers.CharField(
        max_length=255,
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Confirm Password"},
    )


class OTPSerializer(serializers.Serializer):
    """Serializer to validate the otp code and user via email"""

    email = serializers.EmailField(max_length=255, required=True)
    otp_code = serializers.CharField(required=True, max_length=6)


class ResendOTPSerializer(serializers.Serializer):
    """Serializer to resend OTP code to user's email"""

    email = serializers.EmailField(max_length=255, required=True)


class SuspendUserSerializer(serializers.Serializer):
    """Serializer to suspend a user"""

    username = serializers.CharField(max_length=255, required=True)
    is_active = serializers.BooleanField(required=True)
