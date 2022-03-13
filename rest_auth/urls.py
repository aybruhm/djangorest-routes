from rest_auth.views import (
    RegisterOniichan, 
    ChangeUserPasswordAPIView, Konnichiwa,
    LogOniichan, email_otp_verify
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from django.urls import path

app_name = 'authentication'

urlpatterns = [
    path("", Konnichiwa.as_view(), name="welcome"),
    path("register/", RegisterOniichan.as_view(), name="register_user"),
    path("login/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("suspend_user/<str:email>/", SuspendUserApiView.as_view(), name="suspend_user"), 
    path("change_password/<str:email>/", ChangeUserPasswordAPIView.as_view(), name="change_user_password"),
    path("logout/", LogOniichan.as_view(), name="logout_user"),
    
    
    # Email 
    path("otp_verify/", email_otp_verify, name="email_otp_verify    ")
]