from rest_auth.views import (
    AuthViewSet, SuspendUserApiView, 
    ChangeUserPasswordAPIView, Konnichiwa
)
from django.urls import path
# from rest_framework import routers

app_name = 'authentication'

# router = routers.DefaultRouter(trailing_slash=True)

# router.register('', AuthViewSet, basename='auth')

urlpatterns = []

urlpatterns += path("suspend_user/<str:email>/", SuspendUserApiView.as_view(), name="suspend_user"),
urlpatterns += path("change_password/<str:email>/", ChangeUserPasswordAPIView.as_view(), name="change_user_password"),
urlpatterns += path("", Konnichiwa.as_view(), name="welcome"),