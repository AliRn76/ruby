from pv.exceptions import YouDontHaveAccessToThisPV
from pv.models import PVMessage, PV
from rest_framework import serializers


class PVMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PVMessage
        exclude = ['user_id']

    def validate_pv_room_id(self, pv_room_id):
        pv = PV.check_user_access(self.context['request'].user, pv_room_id)
        if pv is None:
            raise YouDontHaveAccessToThisPV
        return pv

    def validate_pv_message_id(self, pv_message_id):
        PVMessage.objects.get_or_raise(id=pv_message_id, pv_room_id=self.data['pv_room_id'])
        return pv_message_id

    def validate(self, attrs):
        attrs['user_id'] = self.context['request'].user
        return attrs

    def to_representation(self, instance):
        return {}
