# Rest Framework Imports
from rest_framework import status, views, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.request import Request

# Simple JWT Imports
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

# DRF YASG Imports
from drf_yasg.utils import swagger_auto_schema

# Third Party Imports
from rest_api_payload import success_response, error_response

# Rest Auth Imports
from rest_routes.utils import send_html_to_email
from rest_routes.serializers import (
    CompleteResetPasswordOTPSerializer,
    RegisterUserSerializer,
    ChangeUserPasswordSerializer,
    OTPSerializer,
    ResendOTPSerializer,
    ResetPasswordOTPSerializer,
    SuspendUserSerializer,
    UserLoginObtainPairSerializer,
    UserSerializer,
)
from rest_routes.permissions import can_suspend_user_perm
from rest_routes.otp_verifications import OTPVerification


# Django Imports
from django.contrib.auth import get_user_model, logout, hashers
from django.shortcuts import render


# Class Initialize
otp_verify = OTPVerification()
User = get_user_model()


class Hello(views.APIView):

    PROTOCOL = "http://"

    def get(self, request: Request) -> Response:

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
                "change_password": BASE_URL
                + "rest_routes/change_password/<str:email>/",
                "reset_password_otp (otp)": BASE_URL
                + "rest_routes/password_reset_otp/",
                "reset_password_otp_confirm (otp)": BASE_URL
                + "rest_routes/password_reset_otp/confirm/",
                "reset_password_otp_complete (otp)": BASE_URL
                + "rest_routes/password_reset_otp/complete/",
                "suspend_user": BASE_URL + "rest_routes/suspend_user/<str:email>/",
            },
        }
        return Response(data=welcome_data, status=status.HTTP_200_OK)


class RegisterUser(views.APIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request: Request) -> Response:
        """
        It creates a new user.

        :param request: Request
        :type request: Request
        :return: A JSON response with a status code and a message.
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()

            payload = success_response(
                status=True,
                message="An OTP code has been sent to your email address!",
                data=serializer.data,
            )
            return Response(data=payload, status=status.HTTP_201_CREATED)

        payload = error_response(status=False, message=serializer.errors)
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(TokenObtainPairView):
    """Inherits TokenObtainPairView from rest_framework simplejwt"""

    serializer_class = UserLoginObtainPairSerializer


class RefreshLoginUser(TokenRefreshView):
    """Inherits TokenRefreshView from rest_framework simplejwt"""

    serializer_class = TokenRefreshSerializer


class ConfirmUserOTP(views.APIView):
    serializer_class = OTPSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            # Get serialized data
            otp_data = serializer.data

            try:
                user = User.objects.get(email=otp_data.get("email"))
            except User.DoesNotExist:
                raise exceptions.PermissionDenied("Credentials does not match our record!")

            if user.is_email_active is False:

                # verifies the otp
                otp_valid = otp_verify.verify_otp_code_from_email(
                    otp_code=otp_data.get("otp_code"), 
                    email=otp_data.get("email")
                )

                if otp_valid is True:

                    user_email = otp_data.get("email")
                    context = {"firstname": user.firstname}

                    # sends welcome email to user
                    send_html_to_email(
                        to_list=[user_email],
                        subject="WELCOME",
                        template_name="emails/users/welcome.html",
                        context=context,
                    )

                    payload = success_response(
                        status=True, 
                        message="OTP code has been verified!", 
                        data={}
                    )
                    return Response(data=payload, status=status.HTTP_202_ACCEPTED)

                payload = error_response(status=False, message="OTP code incorrect. Try again!")
                return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

            elif user.is_active == True and user.is_email_active == True:
                
                payload = success_response(
                    status=True, 
                    message="You are already verified!", 
                    data={}
                )
                return Response(data=payload, status=status.HTTP_200_OK)


class ResendUserOTP(views.APIView):
    serializer_class = ResendOTPSerializer
    permission_classes = [AllowAny]

    def get_user(self, email: str):
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
            raise exceptions.PermissionDenied("Credentials does not match our record!")

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            # Get serialized data
            otp_data = serializer.data
            user = self.get_user(email=otp_data.get("email"))

            if user.is_active and user.is_email_active:

                payload = success_response(
                    status=True, 
                    message="You are already verified!", 
                    data={}
                )
                return Response(data=payload, status=status.HTTP_200_OK)

            elif user.is_email_active is False:

                # Send otp code to user's email address
                otp_sent = otp_verify.send_otp_code_to_email(
                    email=otp_data.get("email"), 
                    first_name=user.firstname
                )

                if otp_sent is not None:

                    payload = success_response(
                        status=True,
                        message="An OTP code has been sent to the provided email address.",
                        data={},
                    )
                    return Response(data=payload, status=status.HTTP_201_CREATED)
                
                payload = error_response(status=False, message="Couldn't sent OTP to user's email address.")
                return Response(data=payload, status=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            payload = error_response(status=False, message=serializer.errors)
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class SuspendUser(views.APIView):
    permissions_classes = (IsAuthenticated, )
    user_serializer = UserSerializer
    suspend_user_serializer = SuspendUserSerializer

    def get_single_user(self, email: str):

        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            raise exceptions.PermissionDenied("Credentials does not match our record!")

    def get(self, request: Request, email: str) -> Response:
        user = self.get_single_user(email=email)
        serializer = self.user_serializer(user)

        payload = success_response(
            status=True, 
            message="User retrieved!", 
            data=serializer.data
        )
        return Response(data=payload, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=suspend_user_serializer)
    def put(self, request: Request, email: str) -> Response:
        user = self.get_single_user(email=email)
        serializer = self.suspend_user_serializer(user, data=request.data)

        """
        Check if the serializer is valid and the user 
        making the request has permission to suspend a user
        """
        if (serializer.is_valid() == True \
            and can_suspend_user_perm(request=request) is True):

            is_active = serializer.validated_data.get("is_active")

            if is_active is False:

                user.is_active = False
                user.save(update_fields=["is_active"])

                payload = success_response(
                    status=True,
                    message="User has been suspended!",
                    data={
                        "user": self.user_serializer(user).data,
                        "user_meta": serializer.data,
                    },
                )
                return Response(data=payload, status=status.HTTP_202_ACCEPTED)

            elif is_active is True:

                user.is_active = True
                user.save(update_fields=["is_active"])

                payload = success_response(
                    status=True,
                    message="User has been activated!",
                    data=serializer.data,
                )
                return Response(data=payload, status=status.HTTP_202_ACCEPTED)

        elif can_suspend_user_perm(request=request) is False:

            payload = error_response(
                status=False,
                message="You don't have the required permission to perform this action!",
            )
            return Response(data=payload, status=status.HTTP_401_UNAUTHORIZED)

        else:
            payload = error_response(status=False, message=serializer.errors)
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class ChangeUserPassword(views.APIView):
    permissions_classes = (IsAuthenticated, )
    serializer_class = ChangeUserPasswordSerializer

    def get_current_user(self, email: str):
        """
        It gets the current user.

        :param email: The email of the user you want to get
        :type email: str
        :return: A user object
        """

        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            raise exceptions.PermissionDenied("Credentials does not match our record!")

    @swagger_auto_schema(request_body=serializer_class)
    def put(self, request: Request, email: str) -> Response:
        user = self.get_current_user(email=email)
        serializer = self.serializer_class(user, data=request.data)

        if serializer.is_valid():

            current_password = serializer.validated_data.get("current_password")
            new_password = serializer.validated_data.get("new_password")

            """
            If the user password equals the current password, 
            set the variable to True, else set it to False
            """
            can_change_password = (
                True
                if hashers.check_password(current_password, user.password)
                else False
            )

            # update user password
            if can_change_password is True:
                user.password = new_password
                user.set_password(new_password)
                user.save(update_fields=["password"])

                payload = success_response(
                    status=True, 
                    message="Password changed!", 
                    data={}
                )
                return Response(data=payload, status=status.HTTP_202_ACCEPTED)

            payload = error_response(
                status=False,
                message="Password incorrect. Please try again!",
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

        payload = error_response(status=False, message=serializer.errors)
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class ResetUserPasswordOTP(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordOTPSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            # Get serialized data
            otp_data = serializer.data

            # Send otp code to user's email address
            otp_sent = otp_verify.send_password_reset_otp_code_to_email(
                email=otp_data.get("email")
            )

            # Check if otp has been sent, then send a response message
            if otp_sent:

                payload = success_response(
                    status=True,
                    message="An OTP code has been sent to the provided email address.",
                    data={},
                )
                return Response(data=payload, status=status.HTTP_202_ACCEPTED)

        else:

            """Else, return a response message telling them to try again"""
            payload = error_response(status=False, message=serializer.errors)
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class ConfirmResetUserPasswordOTP(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = OTPSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            otp_data = serializer.data
            otp_valid = otp_verify.verify_otp_code_from_email(
                otp_code=otp_data.get("otp_code"), 
                email=otp_data.get("email")
            )

            if otp_valid is True:
                user_email = otp_data.get("email")
                user = User.objects.get(email=user_email)
                context = {"firstname": user.firstname}

                # send password reset success email to user
                send_html_to_email(
                    to_list=[user_email],
                    subject="WELCOME BACK, {}".format(user.firstname),
                    template_name="emails/users/welcome.html",
                    context=context,
                )

                payload = success_response(
                    status=True, 
                    message="OTP code has been verified!", 
                    data={}
                )
                return Response(data=payload, status=status.HTTP_202_ACCEPTED)
            
            payload = error_response(status=False, message="OTP code incorrect. Try again!")
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

        else:
            payload = error_response(status=False, message=serializer.errors)
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class ResetUserPasswordOTPComplete(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = CompleteResetPasswordOTPSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            
            # Get data from serializer
            email = serializer.data.get("email")
            password = serializer.data.get("password")

            user = User.objects.get(email=email)
            user.password = password
            user.set_password(password)
            user.save(update_fields=["password"])

            payload = success_response(
                status=True, 
                message="Password reset successful!", 
                data={}
            )
            return Response(data=payload, status=status.HTTP_202_ACCEPTED)

        else:
            payload = error_response(status=False, message=serializer.errors)
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class LogUserOut(views.APIView):
    """
    Removes the authenticated user's ID from the request and flushes their
    session data.
    """

    def post(self, request: Request) -> Response:
        logout(request)

        payload = success_response(
            status=True, 
            message="You logged out!", 
            data={}
        )
        return Response(data=payload, status=status.HTTP_204_NO_CONTENT)


def email_otp_verify(request):
    return render(request, "emails/authentication/otp_verify.html")


def welcome_user(request):
    return render(request, "emails/users/welcome.html")
