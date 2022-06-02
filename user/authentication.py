import time
from .models import User
from datetime import timedelta
from configs.settings import SECRET_KEY
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from jose import jwt, ExpiredSignatureError, JOSEError
from rest_framework.authentication import BaseAuthentication, get_authorization_header


class JWTAuthentication(BaseAuthentication):
    keyword = 'Bearer'
    algorithm = 'HS256'
    model = User

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    @classmethod
    def authenticate_credentials(cls, token):
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[cls.algorithm])
        except ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(_('Token is expired.'))
        except JOSEError:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        try:
            user = cls.model.objects.get(id=decoded_token['user_id'])
        except cls.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if user.is_banned:
            raise exceptions.AuthenticationFailed(_('User is banned.'))

        return user, token

    @staticmethod
    def encode_jwt_token(user: User):
        access_payload = {
            'user_id': user.id,
            'exp': time.time() + timedelta(days=7).total_seconds()
        }
        refresh_payload = {
            'user_id': user.id,
            'exp': time.time() + timedelta(days=30).total_seconds()
        }
        tokens = {
            'access_token': jwt.encode(access_payload, SECRET_KEY, JWTAuthentication.algorithm),
            'refresh_token': jwt.encode(refresh_payload, SECRET_KEY, JWTAuthentication.algorithm),
        }
        return tokens

    def authenticate_header(self, request):
        return self.keyword
