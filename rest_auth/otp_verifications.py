from random import choices
from django.contrib.auth import get_user_model

from rest_auth.utils import send_html_to_email


User = get_user_model()


class OTPVerification:

    DIGITS = "1234567890"
    EXPIRE_TIME = 300

    def generate_otp_code(self, email):

        """Get user email"""
        user = User.objects.get(email=email)

        """Confirm if user exists"""
        if user:

            """Generates an OTP code for the user"""
            user_otp = "".join(choices(self.DIGITS * 2, k=6))
            user.otp_code = user_otp

            """Saves otp code"""
            user.save()
            otp_code = user.otp_code
            return otp_code

    def send_otp_code_to_email(self, email, first_name=None):
        """Generate user otp code"""
        otp_code = self.generate_otp_code(email=email)
        
        """Gets current email making request"""
        user = User.objects.get(email=email)
        
        """context for email template"""
        context = {
            "firstname": None if user.firstname is None else "",
            "otp_code": user.otp_code.id
        }
        
        """Send otp html email to user"""
        send_html_to_email(
            to_list=[user.email], 
            subject="Django Rest Auth - VERIFY YOUR ACCOUNT",
            template_name="emails/authentication/otp_verify.html", 
            context=context,
        )
        return otp_code

    def verify_otp_code_from_email(self, otp_code, email):

        """Get user email"""
        user = User.objects.get(email=email)

        """Check if otp code matches with the user otp code hash id"""
        if int(otp_code) == user.otp_code.id:
            user.is_active = True
            user.is_email_active = True
            user.save()
            return True

    def destroy_otp_code(self, email:str):

        """Get user email"""
        user = User.objects.get(email=email)

        """Destroys user otp code"""
        user.otp_code = ""
        user.save()
        otp_code = user.otp_code
        return otp_code