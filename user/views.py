from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from user.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from user.serializers import RegisterSerializer, LoginSerializer


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.user.last_login = timezone.now()
        serializer.user.save(update_fields=['last_login'])
        tokens = JWTAuthentication.encode_jwt_token(user=serializer.user)
        return Response(data=tokens, status=status.HTTP_202_ACCEPTED)


class RefreshTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        tokens = JWTAuthentication.encode_jwt_token(self.request.user)
        return Response(data=tokens, status=status.HTTP_202_ACCEPTED)
