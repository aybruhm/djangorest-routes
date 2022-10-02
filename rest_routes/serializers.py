# Django Imports
from django.contrib.auth import get_user_model
from django.db.models import Q

# Rest Framework Imports
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Third Party Imports
from rest_api_payload import success_response, error_response

# Rest routes Imports
from rest_routes.otp_verifications import OTPVerification


# Class Instantiations
otp_verify = OTPVerification()
User = get_user_model()


class BaseSerializer(serializers.Serializer):
    """Abstract base serializer to validate email"""
    
    def validate_email(self, value):
        """
        Validate that a user with the email address does not exist.

        Raises:
            serializers.ValidationError: error message

        Returns:
            str: value of email address
        """
        
        user = User.objects.filter(Q(email__iexact=value)).exists()

        if not user:
            raise serializers.ValidationError("User does not exist.")
        return value
    

class PasswordBaseSerializer(BaseSerializer):
    """Password base serializer to validate password(s)"""
    
    def validate(self, attrs):
        
        # get passwords from attrs
        new_password = attrs.get("new_password")
        repeat_password = attrs.get("repeat_new_password")
        
        # validate if passwords are incorrect
        if new_password != repeat_password:
            raise serializers.ValidationError("Password incorrect. Try again!")
        return super().validate(attrs)


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
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Create a new user

        :param validated_data: The data that was sent to the server
        :return: The user object.
        """
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()

        # send otp code to user's email address
        otp_sent = otp_verify.send_otp_code_to_email(
            email=user.email, first_name=user.firstname
        )

        if otp_sent is not None:
            return user
        raise exceptions.ErrorDetail("Couldn't sent OTP to user's email address.")


class UserLoginObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        """The default result (access/refresh tokens)"""
        data = super(UserLoginObtainPairSerializer, self).validate(attrs)

        # check if user is not active
        if self.user.is_active is False:

            payload = error_response(
                status=False,
                message="Account not activated. Kindly request for an activation link.",
            )
            return payload

        # check if user is suspended
        if self.user.is_suspended is True:

            payload = success_response(
                status=True,
                message="Account suspended. Kindly reach out to the support team.",
                data={},
            )
            return payload

        # Added custom data to token serializer
        data.update({"firstname": self.user.firstname})
        data.update({"lastname": self.user.lastname})
        data.update({"username": self.user.username})
        data.update({"email": self.user.email})
        data.update({"id": self.user.id})

        payload = success_response(status=True, message="Login successful", data=data)
        return payload


class ChangeUserPasswordSerializer(PasswordBaseSerializer):
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


class ResetPasswordOTPSerializer(BaseSerializer):
    """Serializer to reset password using OTP"""

    email = serializers.EmailField(max_length=255, required=True)


class CompleteResetPasswordOTPSerializer(PasswordBaseSerializer):
    """Serializer to change password after OTP validation for reset password"""

    email = serializers.EmailField(max_length=255, required=True)
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


class OTPSerializer(BaseSerializer):
    """Serializer to validate the otp code and user via email"""

    email = serializers.EmailField(max_length=255, required=True)
    otp_code = serializers.CharField(required=True, max_length=6)


class ResendOTPSerializer(BaseSerializer):
    """Serializer to resend OTP code to user's email"""

    email = serializers.EmailField(max_length=255, required=True)


class SuspendUserSerializer(serializers.Serializer):
    """Serializer to suspend a user"""

    is_active = serializers.BooleanField(required=True)
