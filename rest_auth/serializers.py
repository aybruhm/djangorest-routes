from rest_auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_api_payload import success_response



class UserSerializer(serializers.ModelSerializer):
    """Serializer that displays a user information"""

    class Meta:
        model = User
        fields = ["id", "firstname", "lastname", "email"]
        extra_kwargs = {
            "email": {
                "read_only": True
            }
        }


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for registering a user"""

    class Meta:
        model = User
        fields = ("firstname", "lastname", "email", "password", "phone_number")
        extra_kwargs = {
            "password": {"write_only": True}
        }


class UserLoginSerializer(serializers.Serializer):
    """Serializer for loggin in user"""
    email = serializers.EmailField(max_length=300, required=True)
    password = serializers.CharField(required=True)
    

class UserLoginObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        """The default result (access/refresh tokens)"""
        data = super(UserLoginObtainPairSerializer, self).validate(attrs)
        
        """Custom data you want to include"""
        data.update({'email': self.user.email})
        data.update({'firstname': self.user.firstname})
        data.update({'lastname': self.user.lastname})
        data.update({'id': self.user.id})
        
        """and everything else you want to send in the response"""
        payload = success_response(
            status="success",
            message="Login successful",
            data=data
        )
        return payload
    

class ChangeUserPasswordSerializer(serializers.Serializer):
    """Serializer to change user password"""
    email = serializers.EmailField(required=True)
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    repeat_new_password = serializers.CharField(required=True)
    
    
class ResetPasswordOTPSerializer(serializers.Serializer):
    """Serializer to reset password using OTP"""
    email = serializers.EmailField(max_length=255, required=True)
    
    
class CompleteResetPasswordOTPSerializer(serializers.Serializer):
    """Serializer to change password after OTP validation for reset password"""
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)
    confirm_password = serializers.CharField(max_length=255, required=True)


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