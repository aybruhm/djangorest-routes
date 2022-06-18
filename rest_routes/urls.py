from rest_routes.views import (
    RegisterUser,
    ConfirmUserOTP,
    ResendUserOTP,
    LoginUser,
    RefreshLoginUser,
    ChangeUserPassword,
    Hello,
    LogUserOut,
    SuspendUser,
    email_otp_verify,
    ResetUserPasswordOTPAPIView,
    ConfirmResetUserPasswordOTPAPIView,
    ResetUserPasswordOTPCompleteAPIView,
    welcome_user,
)
from django.urls import path

app_name = "authentication"

urlpatterns = [
    path("", Hello.as_view(), name="welcome"),
    path("register/", RegisterUser.as_view(), name="register_user"),
    path("login/token/", LoginUser.as_view(), name="login"),
    path("login/refresh/", RefreshLoginUser.as_view(), name="login_refresh"),
    path("confirm_otp/", ConfirmUserOTP.as_view(), name="confirm_otp"),
    path("resend_otp_code/", ResendUserOTP.as_view(), name="resend_otp_code"),
    path(
        "password_reset_otp/",
        ResetUserPasswordOTPAPIView.as_view(),
        name="password_reset_otp",
    ),
    path(
        "password_reset_otp/confirm/",
        ConfirmResetUserPasswordOTPAPIView.as_view(),
        name="password_reset_otp_confirm",
    ),
    path(
        "password_reset_otp/complete/",
        ResetUserPasswordOTPCompleteAPIView.as_view(),
        name="password_reset_otp_confirm",
    ),
    path("suspend_user/<str:email>/", SuspendUser.as_view(), name="suspend_user"),
    path(
        "change_password/<str:email>/",
        ChangeUserPassword.as_view(),
        name="change_user_password",
    ),
    path("logout/", LogUserOut.as_view(), name="logout_user"),
    # Email
    path("otp_verify/", email_otp_verify, name="email_otp_verify "),
    path("welcome/", welcome_user, name="welcome_user"),
]
