from django.urls import path
from user.views import RegisterAPIView, LoginAPIView, RefreshTokenAPIView, ProfileAPIView, MyProfileAPIView, \
    ProfilePictureAPIView, RoomsAPIView, RetrieveUpdateRoomAPIView, ContactAPIView, SubmitPhoneAPIView, SubmitOTPAPIView, \
    ForgetPasswordAPIView, NewPasswordAPIView, CheckUsernameAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('check-username/', CheckUsernameAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('refresh/', RefreshTokenAPIView.as_view()),

    path('submit-phone/', SubmitPhoneAPIView.as_view(http_method_names=['patch'])),
    path('submit-otp/', SubmitOTPAPIView.as_view()),

    path('forget-password/', ForgetPasswordAPIView.as_view()),
    path('new-password/', NewPasswordAPIView.as_view()),

    path('profile/', MyProfileAPIView.as_view()),
    path('profile/<int:user_id>/', ProfileAPIView.as_view()),
    path('profile/picture/', ProfilePictureAPIView.as_view()),

    path('room/', RoomsAPIView.as_view()),
    path('room/<int:user_room_id>/', RetrieveUpdateRoomAPIView.as_view()),

    path('contact/', ContactAPIView.as_view()),
]
