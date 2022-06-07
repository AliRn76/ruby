from django.urls import path
from user.views import RegisterAPIView, LoginAPIView, RefreshTokenAPIView, ProfileAPIView, MyProfileAPIView, \
    ProfilePictureAPIView, RoomsAPIView, UpdateRoomAPIView, ContactAPIView, SubmitPhoneAPIView, SubmitOTPAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('submit-phone/', SubmitPhoneAPIView.as_view()),
    path('submit-otp/', SubmitOTPAPIView.as_view()),
    path('refresh/', RefreshTokenAPIView.as_view()),

    path('profile/', MyProfileAPIView.as_view()),
    path('profile/<int:user_id>/', ProfileAPIView.as_view()),
    path('profile/picture/', ProfilePictureAPIView.as_view()),

    path('room/', RoomsAPIView.as_view()),
    path('room/<int:user_room_id>/', UpdateRoomAPIView.as_view()),

    path('contact/', ContactAPIView.as_view()),
]
