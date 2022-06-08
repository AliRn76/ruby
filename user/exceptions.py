from rest_framework import status
from rest_framework.exceptions import APIException
from configs.messages import WRONG_OTP


class UsernameOrPasswordIsNotCorrect(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Username Or Password Is Not Correct.'


class UsernameAlreadyExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Username Already Exists.'


class OTPIsNotValid(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = WRONG_OTP
