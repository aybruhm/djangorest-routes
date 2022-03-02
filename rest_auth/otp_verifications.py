from random import choices
from django.contrib.auth import get_user_model

from rest_auth.utils import send_html_to_email


User = get_user_model()


class OTPVerification:

    DIGITS = "1234567890"
    EXPIRE_TIME = 300

    def generate_otp_code(self, email):

        # Get user by their unique username
        user = User.objects.get(email=email)

        # Checks if the user exists
        if user:

            # Generates an OTP code for the user
            user_otp = "".join(choices(self.DIGITS * 2, k=6))
            user.otp_code = user_otp

            # Saves OTP code to user table
            user.save()
            otp_code = user.otp_code
            return otp_code

    def send_otp_code_to_email(self, email, first_name=None):
        otp_code = self.generate_otp_code(email=email)
        
        # ------------------------------------------
        # Gets user email
        # ------------------------------------------
        user = User.objects.get(email=email)
        
        # Email context
        context = {
            "firstname": user.firstname,
            "otp_code": user.otp_code.id
        }
        
        # ------------------------------------------
        # Send Welcome HTML Email Template to user
        # ------------------------------------------
        send_html_to_email(
            to_list=[user.email], subject="VERIFY YOUR ACCOUNT",
            template_name="emails/users/verify.html", 
            context=context,
        )
        
        return otp_code

    def verify_otp_code_from_email(self, otp_code, email):

        # Get user by their unique email
        user = User.objects.get(email=email)

        # If the coming otp_code matches the user otp_code id, verify
        if int(otp_code) == user.otp_code.id:
            user.is_active = True
            user.is_email_active = True
            user.save()
            
            return True

    def destroy_otp_code(self, username):

        # Get user by their unique username
        user = User.objects.get(username=username)

        # Destroys otp code
        user.otp_code = ""
        user.save()
        otp_code = user.otp_code
        return otp_code