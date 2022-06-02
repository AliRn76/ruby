from django.db import models
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.exceptions import APIException

class BaseManager(models.Manager):
    def get_or_raise(self, *args, **kwargs):
        queryset = super().get_queryset()
        try:
            return queryset.get(*args, **kwargs)
        except queryset.model.DoesNotExist:
            raise APIException(code=HTTP_404_NOT_FOUND, detail=f'{queryset.model._meta.object_name} Does Not Exist')


