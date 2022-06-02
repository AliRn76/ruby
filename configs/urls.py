from django.contrib import admin
from rest_framework.response import Response
from django.urls import path, include, re_path
from rest_framework.decorators import api_view


@api_view(['POST', 'GET', 'DELETE', 'PUT'])
def _404_not_found(*args, **kwargs):
    return Response(status=404)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('pv/', include('pv.urls')),
    re_path(r'^.*$', _404_not_found),
]
