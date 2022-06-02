from django.urls import path
from user.views import RegisterAPIView, LoginAPIView, RefreshTokenAPIView, ProfileAPIView, MyProfileAPIView, \
    ProfilePictureAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('refresh/', RefreshTokenAPIView.as_view()),

    path('profile/', MyProfileAPIView.as_view()),
    path('profile/<int:user_id>/', ProfileAPIView.as_view()),
    path('profile/picture/', ProfilePictureAPIView.as_view()),
]
