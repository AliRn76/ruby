from rest_framework import status
from rest_framework.exceptions import APIException


class UsernameOrPasswordIsNotCorrect(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Username Or Password Is Not Correct.'
