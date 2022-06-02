from rest_framework import status
from rest_framework.exceptions import APIException


class PVAlreadyExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'PV Already Exists.'


class YouDontHaveAccessToThisPV(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You Don't Have Access To This PV"
