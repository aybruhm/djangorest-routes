# -------------------
# Python -> Imports
# -------------------
from django.http import HttpRequest

# ------------------------------
# Local app -> Django Imports
# ------------------------------
from django.contrib.auth import authenticate, get_user_model, \
    logout, login, hashers
from django.core.exceptions import ImproperlyConfigured

# -----------------------------------------------------
# Installed third-party app -> Rest Framework Imports
# -----------------------------------------------------
from rest_framework import status, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

# -----------------------------------
# Custom app -> Core Imports
# -----------------------------------
from rest_api_payload import success_response, error_response

from rest_auth.serializers import (
    AuthUserSerializer, ChangeUserPasswordSerializer, 
    EmptySerializer, \
    OTPSerializer, ResendOTPSerializer,
    SuspendUserSerializer, UserLoginSerializer, 
    UserSerializer)
from rest_auth.utils import create_user_account, generate_access_token, \
    generate_refresh_token, has_controller_perm_func, send_html_to_email
from rest_auth.otp_verifications import OTPVerification


otp_verify = OTPVerification()
User = get_user_model()


class Konnichiwa(views.APIView):
    
    PROTOCOL = "http://"
    HOST_NAME = "127.0.0.1:8000/"
    BASE_URL = PROTOCOL + HOST_NAME
    
    def get(self, request:HttpRequest) -> Response:
                
        welcome_data = {
            "yoshi!": "If you made it here, I'm proud of you!",
            "message": "I'd love to let you access all this endpoint without being an otaku, \
                    but unfortunately, you just have to be one! Quickly register, \
                        login to access all the endpoints!",
            "routes": {
                "register": self.BASE_URL + "rest_auth/register/",
                "login": self.BASE_URL + "rest_auth/login/",
                "confirm_otp": self.BASE_URL + "rest_auth/confirm_otp/",
                "resend_otp_code": self.BASE_URL + "rest_auth/resend_otp_code/",
                "logout": self.BASE_URL + "rest_auth/logout/",
                "change_password": self.BASE_URL + "rest_auth/change_password/<str:email>/",
                "reset_password": self.BASE_URL + "rest_auth/reset_password/<str:email>/",
                "suspend_user": self.BASE_URL + "rest_auth/suspend_user/<str:email>/"
            }
        }
        return Response(data=welcome_data, status=status.HTTP_200_OK)


class AuthViewSet(GenericViewSet):
    permissions_classes = [AllowAny, ]
    serializer_class = EmptySerializer
    serializer_classes = {
        "login": UserLoginSerializer,
        "register": AuthUserSerializer,
        "confirm_otp_code": OTPSerializer,
        "resend_otp_code": ResendOTPSerializer,
    }

    @action(methods=["GET", "POST"], detail=False)
    def register(self, request: HttpRequest) -> Response:
        # ---------------------------------------
        # This API view creates a new user
        # ---------------------------------------
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = AuthUserSerializer(user).data

        # -----------------------------------------------------
        # Gets user's email address and first name
        # -----------------------------------------------------
        email = user.email
        first_name = user.firstname

        # --------------------------------------------
        # Send otp code to user's email address
        # --------------------------------------------
        otp_sent = otp_verify.send_otp_code_to_email(
            email=email, first_name=first_name
        )

        # ---------------------------------------------------------------------------
        # Checks if otp code has been sent, return user data and otp success message
        # ---------------------------------------------------------------------------
        if otp_sent:
            
            payload = {
                "status": "success",
                "message": "An OTP code has been sent to the provided email address.",
                "data": data
            }
            
            return Response(data=payload, status=status.HTTP_200_OK)

        else:
            
            payload = {
                "status": "failed",
                "message": "Please retry again"
            }
            
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["GET", "POST"], detail=False, permissions_classes=[AllowAny])
    def login(self, request: HttpRequest) -> Response:
        # ------------------------------------
        # This API view logs a user in
        # ------------------------------------
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # ------------------------------------------------------
        # Saves serialized data to a variable for easy access
        # ------------------------------------------------------
        data = serializer.data

        # ---------------------------------------------------
        # Gets email and password value from serializer data
        # ---------------------------------------------------
        email = data["email"]
        password = data["password"]

        # --------------------------------------------------------
        # Authenticates a user using his/her email and password
        # --------------------------------------------------------
        user = authenticate(username=email, password=password)
        
        # -----------------------------------------------------
        # If user doesn't exist, raise login error response
        # -----------------------------------------------------
        if not user:
            
            payload = {
                "status": "failed",
                "message": "Credentials does not match our record"
            }
            
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
        # ---------------------------------------
        # If user exits, but isn't verified
        # ---------------------------------------
        elif user.is_email_active == False:
            
            payload = {
                "status": "failed",
                "message": "Account is not verified!"
            }
            return Response(data=payload, status=status.HTTP_401_UNAUTHORIZED)
        
        # --------------------------
        # Else, logs the user in
        # --------------------------
        else:
            login(request, user)
            
            # Initiate Response class to a variable
            response = Response()
            
            # --------------------------------------
            # Get access and refresh token for user
            # --------------------------------------
            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)
            
            # --------------------------------------------
            # Returns logged in user data -> information
            # --------------------------------------------
            data = {
                "email": data["email"],
                "password": data["password"],
                "token": access_token
            }
            
            # Set cookie using the refresh token
            response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
            
            payload = {
                "status": "success",
                "message": "Login successful",
                "data": data
            }
            return Response(data=payload, status=status.HTTP_200_OK)

    @action(methods=["GET", "POST"], detail=False, permissions_classes=[AllowAny])
    def confirm_otp_code(self, request: HttpRequest) -> Response:
        # --------------------------------------------------------
        # This API view confirms incoming otp code from the user
        # --------------------------------------------------------
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_data = serializer.data

        # ----------------------------------------------------
        # Capture email from serialized data and fetch user
        # ----------------------------------------------------
        try:
            user = User.objects.get(email=otp_data.get('email'))
        except User.DoesNotExist:
            payload = {
                "status": "failed",
                "message": "Credentials is not in our records!"
            }

        # ----------------------------------------------------------
        # Check if a user active and email active flag is False
        # ----------------------------------------------------------
        if user.is_active == True and user.is_email_active == False:

            # ------------------------------------
            # Verify user with the provided OTP
            # ------------------------------------
            otp_valid = otp_verify.verify_otp_code_from_email(
                otp_code=otp_data.get("otp_code"), email=otp_data.get("email"))
            
            # ----------------------------------------------------------------------------
            # If the otp validation is True, set the user active and email active to True
            # ----------------------------------------------------------------------------
            if otp_valid is True:
                
                # ------------------------------------------
                # Gets user email
                # ------------------------------------------
                user_email = otp_data.get("email")
                
                # Context for html email
                context = {
                    "firstname": user.firstname
                }
                
                # ------------------------------------------
                # Send Welcome HTML Email Template to user
                # ------------------------------------------
                send_html_to_email(
                    to_list=[user_email], subject="WELCOME",
                    template_name="emails/users/welcome.html", 
                    context=context,
                )

                # ---------------------------------------------------------------------------------
                # Return a response message that lets the user know the otp code has been verified
                # ---------------------------------------------------------------------------------
                payload = {
                    "status": "success",
                    "message": "OTP code has been verified!"
                }
                
                return Response(data=payload, status=status.HTTP_202_ACCEPTED)

            else:
                
                # ---------------------------------------------------------------------------------
                # Return a response message that lets the user know the otp code validation failed
                # ---------------------------------------------------------------------------------
                payload = {
                    "status": "failed",
                    "message": "OTP code incorrect. Try again!"
                }
                return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

        elif user.is_active == True and user.is_email_active == True:
            
            # -------------------------------------------------------
            # Let the user know that he/she is verified already
            # -------------------------------------------------------
            payload = {
                "status": "success",
                "message": "You are already verified!"
            }
            return Response(data=payload, status=status.HTTP_200_OK)

    @action(methods=["GET", "POST"], detail=False, permissions_classes=[AllowAny])
    def resend_otp_code(self, request: HttpRequest) -> Response:
        # -------------------------------------------------------
        # This API view resends an otp code to the user's email
        # -------------------------------------------------------
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_data = serializer.data

        # ------------------------------------------------------
        # Capture email from serialized data and fetch user
        # ------------------------------------------------------
        try:
            user = User.objects.get(email=otp_data.get('email'))
        except User.DoesNotExist:
            payload = {
                "status": "failed",
                "message": "Credentials does not match our record!"
            }
            return Response(data=payload, status=status.HTTP_401_UNAUTHORIZED)

        # ------------------------------------------------
        # Checks if user account is already validated
        # ------------------------------------------------
        if user.is_active is True and user.is_email_active is True:
            
            payload = {
                "status": "success",
                "message": "You are already verified!"
            }
            return Response(data=payload,
                            status=status.HTTP_200_OK)

        elif user.is_email_active is False:

            # ----------------------------------------
            # Send otp code to user's email address
            # ----------------------------------------
            otp_sent = otp_verify.send_otp_code_to_email(
                email=otp_data.get("email"), first_name=user.firstname
            )

            # ----------------------------------------------------------
            # Check if otp has been sent, then send a response message
            # ----------------------------------------------------------
            if otp_sent:
                
                payload = {
                    "status": "success",
                    "message": "An OTP code has been sent to the provided email address."
                }
                return Response(data=payload, status=status.HTTP_201_CREATED)

        else:
            # ----------------------------------------------------------
            # Return a response message telling them to try again
            # ----------------------------------------------------------
            payload = {
                "status": "failed",
                "message": "Something went wrong! Please try again."
            }
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST", ], detail=False, permissions_classes=[IsAuthenticated])
    def logout(self, request: HttpRequest) -> Response:
        # ----------------------------------
        # This API view logs a user out
        # ----------------------------------
        logout(request)
        
        payload = {
            "status": "success",
            "message": "Logout successful"
        }
        return Response(data=payload, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
    

class SuspendUserApiView(views.APIView):
    permissions_classes = [IsAuthenticated]
    
    def get_single_user(self, email:str) -> Response:
        
        try: 
            user = User.objects.get(is_active=True, email=email)
            return user
        except User.DoesNotExist:
            payload = error_response(
                status="failed",
                message="User does not exist!"
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request:HttpRequest, email:str) -> Response:
        user = self.get_single_user(email=email)
        serializer = SuspendUserSerializer(user)
        
        payload = success_response(
            status="success",
            message="User retrieved!",
            data=serializer.data
        )
        return Response(data=payload, status=status.HTTP_200_OK)

    def put(self, request:HttpRequest, email:str) -> Response:
        user = self.get_single_user(email=email)
        serializer = SuspendUserSerializer(data=request.data, instance=user)
        
        # Serialized data from the serializer
        serialized_email = serializer.initial_data.get("email")
        serialized_active_flag = serializer.initial_data.get("is_staff")
        
        # Logic to check if the user request has the following perms
        # -> is_staff, is_active, is_authenticated, has_checker_perm
        user_has_checker_perm = has_controller_perm_func(request.user)
        
        # Check if the serializer is valid and 
        # the user making the request has controller permission
        if serializer.is_valid() == user_has_checker_perm is True:
            
            # Checks if the serialized is_active flag is set to True and;
            # the serialized email is equal to the user email
            if serialized_active_flag is True and serialized_email is user.email:
                
                # Suspend the user
                user.is_active = False
                user.save()

                # Custom payload
                payload = success_response(
                    status="success", 
                    message="User successfully suspended!", 
                    data=serializer.data
                )
                return Response(data=payload, status=status.HTTP_202_ACCEPTED)

            # Checks if the serialized is_active flag is set to False and;
            # the serialized email is equal to the user email
            elif serialized_active_flag is False and serialized_email is user.email:
                
                # Activate the user
                user.is_active = True
                user.save()
                
                # Custom payload
                payload = success_response(
                    status="success",
                    message="User successfully activated!",
                    data=serializer.data
                )
                return Response(data=payload, status=status.HTTP_202_ACCEPTED)
        
            payload = error_response(
                success="failed",
                message="User does not have the required permission to perform this action!"
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    
        payload = error_response(
            status="failed",
            message="Something went wrong. Please try again!"
        )
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    
    
class ChangeUserPasswordAPIView(views.APIView):
    permissions_classes = [IsAuthenticated]
    
    def get_current_user(self, email:str) -> Response:
        
        try:
            user = User.objects.get(is_active=True, email=email)
            return user
        except User.DoesNotExist:
            payload = error_response(
                status="404 not found",
                message="User does not exist!"
            )
            return Response(data=payload, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request: HttpRequest, email:str) -> Response:
        user = self.get_current_user(email=email)
        serializer = UserSerializer(user)
        
        payload = success_response(
            status="200 ok",
            message="User retrieved!",
            data=serializer.data
        )
        return Response(data=payload, status=status.HTTP_200_OK)
    
    def put(self, request:HttpRequest, email:str) -> Response:
        
        # Get current user
        user = self.get_current_user(email=email)
        serializer = ChangeUserPasswordSerializer(user, data=request.data)
        
        if serializer.is_valid():
            
            current_password = serializer.validated_data.get("current_password")
            new_password = serializer.validated_data.get("new_password")
            repeat_new_password = serializer.validated_data.get("repeat_new_password")
            
            """
            If the user password equals the current password, 
            set the variable to True, else set it to False
            """
            can_change_password = True if hashers.check_password(current_password, user.password) else False
            
            """
            If the can change password variable is True, 
            and the new password requals the repeat new password, 
            set the password message to True else False
            """
            password_message = True \
                if can_change_password is True \
                and new_password == repeat_new_password \
                else False
            
            """
            Update current user password
            """
            if password_message is True:
                user.password = new_password
                user.set_password(new_password)
                user.save()
                
                user_new_data = {
                    "password": {
                        "old": current_password,
                        "new": new_password,
                        "new_again": repeat_new_password
                    }
                }
                
                payload = success_response(
                    status="202 accepted",
                    message="User password changed!",
                    data=user_new_data
                )
                return Response(data=payload, status=status.HTTP_202_ACCEPTED)
            
            else:
                
                payload = error_response(
                    status="400 bad request",
                    message="Password incorrect. Please try again!"
                )
                return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            
            payload = error_response(
                status="400 bad request",
                message=serializer.errors
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)