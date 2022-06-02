from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from pv.models import PV
from user.models import User
from pv.serializers import PVMessageSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated


class CreatePVAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        if user_id == self.request.user.id:
            data = {'detail': 'You Can Not Create PV With Yourself.'}
            return Response(data=data, status=status.HTTP_406_NOT_ACCEPTABLE)
        user = User.objects.get_or_raise(id=user_id)
        pv = PV.create_pv(user1=self.request.user, user2=user)
        data = {'pv_id': pv.id}
        return Response(data=data, status=status.HTTP_201_CREATED)


class PVMessageAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PVMessageSerializer

