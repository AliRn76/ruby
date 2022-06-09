from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from configs.messages import SUCCESS_OTP, WRONG_OTP, PASSWORD_CHANGED
from configs.paginations import Pagination
from cache.queries import get_otp, remove_otp, set_forget_password_otp, get_forget_password_otp, \
    remove_forget_password_otp
from configs.settings import OTP_EXP_SECOND
from user.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView, ListAPIView, \
    GenericAPIView

from user.exceptions import OTPIsNotValid
from user.models import User, UserRoom
from user.serializers import (
    ProfilePictureSerializer,
    SubmitPhoneSerializer,
    RegisterSerializer,
    ProfileSerializer,
    LoginSerializer,
    RoomsSerializer,
    ContactSerializer,
    SubmitOTPSerializer, NewPasswordSerializer, CheckUsernameSerializer, ForgetPasswordSerializer,
)
from user.utils import generate_otp


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.user.update_last_login()
        tokens = JWTAuthentication.encode_jwt_token(user=serializer.user)
        return Response(data=tokens, status=status.HTTP_202_ACCEPTED)


class CheckUsernameAPIView(APIView):
    serializer_class = CheckUsernameSerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return Response()


class SubmitPhoneAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmitPhoneSerializer

    def get_object(self, *args, **kwargs):
        return self.request.user


class SubmitOTPAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmitOTPSerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['otp'] == get_otp(self.request.user.id):
            remove_otp(self.request.user.id)
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            data = {'detail': WRONG_OTP}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        tokens = JWTAuthentication.encode_jwt_token(self.request.user)
        return Response(data=tokens, status=status.HTTP_202_ACCEPTED)


class ForgetPasswordAPIView(APIView):
    serializer_class = ForgetPasswordSerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get_or_raise(phone_number=serializer.validated_data['phone_number'])
        set_forget_password_otp(user_id=user.id, otp=generate_otp())
        data = {'detail': SUCCESS_OTP, 'timer': OTP_EXP_SECOND}
        return Response(data=data, status=status.HTTP_200_OK)


class NewPasswordAPIView(APIView):
    serializer_class = NewPasswordSerializer

    def check_otp(self, otp):
        _otp = get_forget_password_otp(user_id=self.user.id)
        if otp == _otp:
            remove_forget_password_otp(user_id=self.user.id)
        else:
            raise OTPIsNotValid

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        self.user = User.objects.get_or_raise(phone_number=serializer.validated_data['phone_number'])
        self.check_otp(serializer.validated_data['otp'])
        self.user.set_password(serializer.validated_data['password'])
        self.user.save(update_fields=['password'])
        data = {'detail': PASSWORD_CHANGED}
        return Response(data=data, status=status.HTTP_200_OK)


class MyProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self, *args, **kwargs):
        return User.objects.get_or_raise(id=self.request.user.id)


class ProfileAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self, *args, **kwargs):
        return User.objects.get_or_raise(id=self.kwargs['user_id'])


class ProfilePictureAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfilePictureSerializer

    def get_object(self, *args, **kwargs):
        return User.objects.get_or_raise(id=self.request.user.id)


class RoomsAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomsSerializer
    pagination_class = Pagination

    def get_queryset(self, *args, **kwargs):
        return UserRoom.objects.filter(~Q(last_message=None), user_id=self.request.user).order_by('-timestamp')


class UpdateRoomAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomsSerializer

    def get_object(self, *args, **kwargs):
        return UserRoom.objects.get_or_raise(~Q(last_message=None), id=self.kwargs['user_room_id'])


class ContactAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data, many=True)
        serializer.is_valid(raise_exception=True)
        data = [
            {d['phone_number']: True} if User.objects.filter(phone_number=d['phone_number']).first() else {d['phone_number']: False}
            for d in serializer.validated_data
        ]
        return Response(data=data, status=status.HTTP_200_OK)

