from django.contrib import admin
from django.urls import path, include

from user.views import RegisterAPIView, LoginAPIView, RefreshTokenAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('refresh/', RefreshTokenAPIView.as_view()),
]
