"""Rest Framework Imports"""
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


"""Third Party Imports"""
from rest_api_payload import success_response, error_response


"""Custom app -> Rest Auth Imports"""
from rest_routes.utils import send_html_to_email
from rest_routes.serializers import (
    CompleteResetPasswordOTPSerializer,
    RegisterUserSerializer,
    ChangeUserPasswordSerializer,
    OTPSerializer,
    ResendOTPSerializer,
    ResetPasswordOTPSerializer,
    UserLoginObtainPairSerializer,
)
from rest_routes.otp_verifications import OTPVerification


"""Django Imports"""
from django.http import HttpRequest
from django.contrib.auth import get_user_model, logout, hashers
from django.shortcuts import render


"""Class Instantiations"""
otp_verify = OTPVerification()
User = get_user_model()


class Konnichiwa(views.APIView):

    PROTOCOL = "http://"

    def get(self, request: HttpRequest) -> Response:

        HOST_NAME = request.get_host() + "/"
        BASE_URL = self.PROTOCOL + HOST_NAME

        welcome_data = {
            "yosh!": "If you made it here, I'm proud of you!",
            "routes": {
                "register": BASE_URL + "rest_routes/register/",
                "login (jwt)": BASE_URL + "rest_routes/login/token/",
                "login (refresh jwt)": BASE_URL + "rest_routes/login/refresh/",
                "confirm_otp": BASE_URL + "rest_routes/confirm_otp/",
                "resend_otp_code": BASE_URL + "rest_routes/resend_otp_code/",
                "logout": BASE_URL + "rest_routes/logout/",
                "change_password": BASE_URL + "rest_routes/change_password/<str:email>/",
                "reset_password_otp (otp)": BASE_URL + "rest_routes/password_reset_otp/",
                "reset_password_otp_confirm (otp)": BASE_URL + "rest_routes/password_reset_otp/confirm/",
                "reset_password_otp_complete (otp)": BASE_URL + "rest_routes/password_reset_otp/complete/",
                "suspend_user": BASE_URL + "rest_routes/suspend_user/<str:email>/",
            },
        }
        return Response(data=welcome_data, status=status.HTTP_200_OK)


class RegisterOniichan(views.APIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest) -> Response:
        """
        It creates a new user.

        :param request: HttpRequest
        :type request: HttpRequest
        :return: A JSON response with a status code and a message.
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()

            payload = success_response(
                status="success",
                message="An OTP code has been sent to your email address!",
                data=serializer.data,
            )
            return Response(data=payload, status=status.HTTP_200_OK)

        payload = error_response(status="failed", message=serializer.errors)
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class LoginOniichan(TokenObtainPairView):
    """Inherits TokenObtainPairView from rest_framework simplejwt"""

    serializer_class = UserLoginObtainPairSerializer


class RefreshLoginOniichan(TokenRefreshView):
    """Inherits TokenRefreshView from rest_framework simplejwt"""

    serializer_class = TokenRefreshSerializer


class ConfirmOniichanOTP(views.APIView):
    serializer_class = OTPSerializer
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            """Get serialized data"""
            otp_data = serializer.data

            """Check to see if user exits"""
            try:
                user = User.objects.get(email=otp_data.get("email"))
            except User.DoesNotExist:
                payload = error_response(
                    status="failed", message="Credentials does not match our record!"
                )
                return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

            """Check if user email active flag is False"""
            if user.is_email_active == False:

                """Verifies user with the provided OTP"""
                otp_valid = otp_verify.verify_otp_code_from_email(
                    otp_code=otp_data.get("otp_code"), email=otp_data.get("email")
                )

                """If the otp validation is True, set the user active and email active to True"""
                if otp_valid is True:

                    """Gets user email"""
                    user_email = otp_data.get("email")

                    """Context for html email"""
                    context = {"firstname": user.firstname}

                    """Sends Welcome HTML Email to user"""
                    send_html_to_email(
                        to_list=[user_email],
                        subject="WELCOME",
                        template_name="emails/users/welcome.html",
                        context=context,
                    )

                    """Return a response message that lets the user know the otp code has been verified"""
                    payload = success_response(
                        status="success", message="OTP code has been verified!", data={}
                    )
                    return Response(data=payload, status=status.HTTP_202_ACCEPTED)

                else:

                    """Return a response message that lets the user know the otp code validation failed"""
                    payload = error_response(
                        status="failed", message="OTP code incorrect. Try again!"
                    )
                    return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

            elif user.is_active == True and user.is_email_active == True:

                """Let the user know that he/she is verified already"""
                payload = success_response(
                    status="success", message="You are already verified!", data={}
                )
                return Response(data=payload, status=status.HTTP_200_OK)


class ResendOniichanOTP(views.APIView):
    serializer_class = ResendOTPSerializer
    permission_classes = [AllowAny]
    
    def get_user(self, email:str):
        """
        Get a user by email
        
        :param email: The email of the user you want to get
        :type email: str
        :return: A user object
        """
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            payload = error_response(
                status="failed", message="Credentials does not match our record!"
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request: HttpRequest) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            """Get serialized data"""
            otp_data = serializer.data

            """Get user"""
            user = self.get_user(email=otp_data.get("email"))

            """Check if a user active and email active flag is True"""
            if user.is_active == True and user.is_email_active == True:

                payload = success_response(
                    status="success", message="You are already verified!", data={}
                )
                return Response(data=payload, status=status.HTTP_200_OK)

            elif user.is_email_active is False:

                """Send otp code to user's email address"""
                otp_sent = otp_verify.send_otp_code_to_email(
                    email=otp_data.get("email"), first_name=user.firstname
                )

                """Check if otp has been sent, then send a response message"""
                if otp_sent:

                    payload = success_response(
                        status="success",
                        message="An OTP code has been sent to the provided email address.",
                        data={},
                    )
                    return Response(data=payload, status=status.HTTP_201_CREATED)

            else:
                """Return a response message telling them to try again"""
                payload = error_response(
                    status="failed", message="Something went wrong! Please try again."
                )
                return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


# class SuspendUserApiView(views.APIView):
#     permissions_classes = [IsAuthenticated]

#     def get_single_user(self, email:str) -> Response:

#         try:
#             user = User.objects.get(is_active=True, email=email)
#             return user
#         except User.DoesNotExist:
#             payload = error_response(
#                 status="failed",
#                 message="User does not exist!"
#             )
#             return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request:HttpRequest, email:str) -> Response:
#         user = self.get_single_user(email=email)
#         serializer = SuspendUserSerializer(user)

#         payload = success_response(
#             status="success",
#             message="User retrieved!",
#             data=serializer.data
#         )
#         return Response(data=payload, status=status.HTTP_200_OK)

#     def put(self, request:HttpRequest, email:str) -> Response:
#         user = self.get_single_user(email=email)
#         serializer = SuspendUserSerializer(data=request.data, instance=user)

#         # Serialized data from the serializer
#         serialized_email = serializer.initial_data.get("email")
#         serialized_active_flag = serializer.initial_data.get("is_staff")

#         # Logic to check if the user request has the following perms
#         # -> is_staff, is_active, is_authenticated, has_checker_perm
#         user_has_checker_perm = has_controller_perm_func(request.user)

#         # Check if the serializer is valid and
#         # the user making the request has controller permission
#         if serializer.is_valid() == user_has_checker_perm is True:

#             # Checks if the serialized is_active flag is set to True and;
#             # the serialized email is equal to the user email
#             if serialized_active_flag is True and serialized_email is user.email:

#                 # Suspend the user
#                 user.is_active = False
#                 user.save()

#                 # Custom payload
#                 payload = success_response(
#                     status="success",
#                     message="User successfully suspended!",
#                     data=serializer.data
#                 )
#                 return Response(data=payload, status=status.HTTP_202_ACCEPTED)

#             # Checks if the serialized is_active flag is set to False and;
#             # the serialized email is equal to the user email
#             elif serialized_active_flag is False and serialized_email is user.email:

#                 # Activate the user
#                 user.is_active = True
#                 user.save()

#                 # Custom payload
#                 payload = success_response(
#                     status="success",
#                     message="User successfully activated!",
#                     data=serializer.data
#                 )
#                 return Response(data=payload, status=status.HTTP_202_ACCEPTED)

#             payload = error_response(
#                 success="failed",
#                 message="User does not have the required permission to perform this action!"
#             )
#             return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

#         payload = error_response(
#             status="failed",
#             message="Something went wrong. Please try again!"
#         )
#         return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class ChangeOniichanPassword(views.APIView):
    permissions_classes = [IsAuthenticated]
    serializer_class = ChangeUserPasswordSerializer

    def get_current_user(self, email: str):
        """
        It gets the current user.

        :param email: The email of the user you want to get
        :type email: str
        :return: A user object
        """

        try:
            user = User.objects.get(is_active=True, email=email)
            return user
        except User.DoesNotExist:
            payload = error_response(
                status="failed", message="Credentials does not match our record!"
            )
            return Response(data=payload, status=status.HTTP_404_NOT_FOUND)

    def put(self, request: HttpRequest, email: str) -> Response:

        """Get current logged in user"""
        user = self.get_current_user(email=email)
        serializer = self.serializer_class(user, data=request.data)

        if serializer.is_valid():

            current_password = serializer.validated_data.get("current_password")
            new_password = serializer.validated_data.get("new_password")
            repeat_new_password = serializer.validated_data.get("repeat_new_password")

            """
            If the user password equals the current password, 
            set the variable to True, else set it to False
            """
            can_change_password = (
                True
                if hashers.check_password(current_password, user.password)
                else False
            )

            """
            If the can change password variable is True, 
            and the new password requals the repeat new password, 
            set the password message to True else False
            """
            password_message = (
                True
                if can_change_password is True and new_password == repeat_new_password
                else False
            )

            """
            Update current user password
            """
            if password_message is True:
                user.password = new_password
                user.set_password(new_password)
                user.save()

                payload = success_response(
                    status="success", message="Password changed!", data={}
                )
                return Response(data=payload, status=status.HTTP_202_ACCEPTED)

            payload = error_response(
                status="failed",
                message="Password incorrect. Please try again!",
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

        payload = error_response(status="failed", message=serializer.errors)
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class ResetOniichanPasswordOTPAPIView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordOTPSerializer

    def post(self, request: HttpRequest) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            """Get serialized data"""
            otp_data = serializer.data

            """Send otp code to user's email address"""
            otp_sent = otp_verify.send_password_reset_otp_code_to_email(
                email=otp_data.get("email")
            )

            """Check if otp has been sent, then send a response message"""
            if otp_sent:

                payload = success_response(
                    status="success",
                    message="An OTP code has been sent to the provided email address.",
                    data={},
                )
                return Response(data=payload, status=status.HTTP_202_ACCEPTED)

        else:

            """Else, return a response message telling them to try again"""
            payload = error_response(status="failed", message=serializer.errors)
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class ConfirmResetOniichanPasswordOTPAPIView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = OTPSerializer

    def post(self, request: HttpRequest) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            """Get serialized data"""
            otp_data = serializer.data

            """Validate otp code"""
            otp_valid = otp_verify.verify_otp_code_from_email(
                otp_code=otp_data.get("otp_code"), email=otp_data.get("email")
            )

            """Checks if otp valid comes out True"""
            if otp_valid is True:

                """Gets user email"""
                user_email = otp_data.get("email")

                """Gets user"""
                user = User.objects.get(email=user_email)

                """Context for html email"""
                context = {"firstname": user.firstname}

                """Send Password Reset Success HTML Email to user"""
                send_html_to_email(
                    to_list=[user_email],
                    subject="WELCOME BACK, {}".format(user.firstname),
                    template_name="emails/users/welcome.html",
                    context=context,
                )

                """Return a response message that lets the user know the otp validation was successful"""
                payload = success_response(
                    status="success", message="OTP code has been verified!", data={}
                )
                return Response(data=payload, status=status.HTTP_202_ACCEPTED)

            else:

                """Return a response message that lets the know that the otp code validation failed"""
                payload = error_response(
                    status="failed", message="OTP code incorrect. Try again!"
                )
                return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class ResetOniichanPasswordOTPCompleteAPIView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = CompleteResetPasswordOTPSerializer

    def post(self, request: HttpRequest) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            """Serialized data"""
            data = serializer.data

            """Get email, password and confirm password"""
            email = data.get("email")
            password = data.get("password")
            confirm_password = data.get("confirm_password")

            """Get user"""
            user = User.objects.get(email=email)

            """Check if password and confirm_password is the same"""
            password_message = True if password == confirm_password else False

            """Check if password message is True, then set and hash user password"""
            if password_message is True:
                user.password = password
                user.set_password(password)
                user.save()

                """Return a response message to the user saying password reset was successful"""
                payload = success_response(
                    status="success", message="Password reset successful!", data={}
                )
                return Response(data=payload, status=status.HTTP_202_ACCEPTED)

            else:

                """Return a response message to the user saying password incorrect"""
                payload = error_response(
                    status="failed",
                    message="Password incorrect. Plelase try again!",
                )
                return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
        else:

            """Return a response message to the user with the error message"""
            payload = error_response(
                status="failed", message=serializer.errors
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class LogOniichanOut(views.APIView):
    """
    Removes the authenticated user's ID from the request and flushes their
    session data.
    """

    response = Response()

    def post(self, request: HttpRequest) -> Response:

        """Flush out user's session from the client side"""
        request.session.flush()

        """Wipes user request"""
        logout(request)

        payload = success_response(
            status="success", message="You logged out!", data={}
        )
        return Response(data=payload, status=status.HTTP_204_NO_CONTENT)


def email_otp_verify(request):
    return render(request, "emails/authentication/otp_verify.html")


def welcome_user(request):
    return render(request, "emails/users/welcome.html")
