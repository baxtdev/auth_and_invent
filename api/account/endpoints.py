from rest_registration.api.views.change_password import ChangePasswordView
from rest_registration.api.views.login import LoginView,LogoutView
from rest_registration.api.views.profile import ProfileView
from rest_registration.api.views.register import RegisterView
from rest_framework.routers import DefaultRouter

from django.urls import path, re_path, include

from api.account.api import ChekingCodeAPI,RegisterAPIView,\
    VeryfiCodeByEmailAPIView,AuthWithCodeAPIView,InviteCodeAPIview,ToInviteCodeAPIView


router = DefaultRouter()


urlpatterns = [
    path('profile/',ProfileView.as_view(),name='user-profile'),
    path('auth/<int:code>',AuthWithCodeAPIView.as_view(),name='reset-password'),
    path('register/',RegisterAPIView.as_view(),name="user-register"),
    path('activate/invitecode/<str:code>',ToInviteCodeAPIView.as_view(),name="activete-invite-code"),
]