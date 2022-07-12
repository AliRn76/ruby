from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from user.models import User
from pv.models import PV, PVMessage
from configs.paginations import Pagination
from pv.serializers import PVMessageSerializer, UpdatePVMessageSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
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


class PVMessageAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PVMessageSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return PVMessage.objects.filter(user_id=self.request.user.id, pv_id=self.kwargs['pv_id'])


class UpdateDestroyPVMessageAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdatePVMessageSerializer

    def get_serializer_context(self):
        context = super(UpdateDestroyPVMessageAPIView, self).get_serializer_context()
        context['pv_id'] = self.kwargs['pv_id']
        return context

    def get_object(self):
        return PVMessage.objects.get_or_raise(id=self.kwargs['pv_message_id'], user_id=self.request.user.id)


class ReadPVMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return PVMessage.objects.get_or_raise(id=self.kwargs['pv_message_id'], user_id=self.request.user.id)

    def post(self, request, *args, **kwargs):
        message = self.get_object()
        message.is_unread = False
        message.save(update_fields=['is_unread'])
        return Response(status=status.HTTP_200_OK)
