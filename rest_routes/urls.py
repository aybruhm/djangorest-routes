from rest_routes.views import (
    RegisterOniichan,
    ConfirmOniichanOTP,
    ResendOniichanOTP,
    LoginOniichan,
    RefreshLoginOniichan,
    ChangeOniichanPassword,
    Konnichiwa,
    LogOniichanOut,
    email_otp_verify,
    ResetOniichanPasswordOTPAPIView,
    ConfirmResetOniichanPasswordOTPAPIView,
    ResetOniichanPasswordOTPCompleteAPIView,
    welcome_user,
)
from django.urls import path

app_name = "authentication"

urlpatterns = [
    path("", Konnichiwa.as_view(), name="welcome"),
    path("register/", RegisterOniichan.as_view(), name="register_user"),
    path("login/token/", LoginOniichan.as_view(), name="login"),
    path("login/refresh/", RefreshLoginOniichan.as_view(), name="login_refresh"),
    path("confirm_otp/", ConfirmOniichanOTP.as_view(), name="confirm_otp"),
    path("resend_otp_code/", ResendOniichanOTP.as_view(), name="resend_otp_code"),
    path(
        "password_reset_otp/",
        ResetOniichanPasswordOTPAPIView.as_view(),
        name="password_reset_otp",
    ),
    path(
        "password_reset_otp/confirm/",
        ConfirmResetOniichanPasswordOTPAPIView.as_view(),
        name="password_reset_otp_confirm",
    ),
    path(
        "password_reset_otp/complete/",
        ResetOniichanPasswordOTPCompleteAPIView.as_view(),
        name="password_reset_otp_confirm",
    ),
    # path("suspend_user/<str:email>/", SuspendUserApiView.as_view(), name="suspend_user"),
    path(
        "change_password/<str:email>/",
        ChangeOniichanPassword.as_view(),
        name="change_user_password",
    ),
    path("logout/", LogOniichanOut.as_view(), name="logout_user"),
    # Email
    path("otp_verify/", email_otp_verify, name="email_otp_verify "),
    path("welcome/", welcome_user, name="welcome_user"),
]
