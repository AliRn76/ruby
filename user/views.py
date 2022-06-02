from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from user.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from user.models import User
from user.serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, ProfilePictureSerializer


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


class RefreshTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        tokens = JWTAuthentication.encode_jwt_token(self.request.user)
        return Response(data=tokens, status=status.HTTP_202_ACCEPTED)


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

