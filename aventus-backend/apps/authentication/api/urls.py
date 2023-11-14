from django.urls import include, path, re_path
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework import routers


urlpatterns = [
    path('initial-registration', views.RegisterAPIView.as_view()),
    path('final-registration', views.FinalRegistrationAPIView.as_view()),
    # path('login_with_mobile', views.LoginWithMobileAPIView.as_view()),
    
    # path('verify_otp', VerifyOTP.as_view()),
    path('login', views.LoginAPIView.as_view()),
    path('logout', views.LogoutAPIView.as_view()),
    path('refresh-token', views.RefreshTokenView.as_view()),
    
    
]
