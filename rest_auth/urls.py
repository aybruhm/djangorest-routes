from rest_auth.views import (
    AuthViewSet, SuspendUserApiView, ChangeUserPasswordAPIView
)
from django.urls import path
from rest_framework import routers

app_name = 'authentication'

router = routers.DefaultRouter(trailing_slash=True)

router.register('', AuthViewSet, basename='auth')

urlpatterns = router.urls

urlpatterns += path("suspend_user/<str:username>/", SuspendUserApiView.as_view(), name="suspend-user"),
urlpatterns += path("change_password/<str:email>/", ChangeUserPasswordAPIView.as_view(), name="change_user_password"),