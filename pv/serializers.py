from pv.exceptions import YouDontHaveAccessToThisPV
from pv.models import PVMessage, PV
from rest_framework import serializers


class PVMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PVMessage
        fields = '__all__'
        read_only_fields = ('user_id', 'is_unread')

    def validate_pv_room_id(self, pv_room_id):
        pv = PV.check_user_access(self.context['request'].user, pv_room_id)
        if pv is None:
            raise YouDontHaveAccessToThisPV
        return pv

    def validate_reply_id(self, reply_id):
        PVMessage.objects.get_or_raise(id=reply_id, pv_id=self.data['pv_id'])
        return reply_id

    def validate(self, attrs):
        attrs['user_id'] = self.context['request'].user
        return attrs

    def to_representation(self, instance):
        if self.context['request'].method == 'GET':
            return super(PVMessageSerializer, self).to_representation(instance)
        else:
            return {}


class UpdatePVMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PVMessage
        fields = ['text', 'image', 'reply_id']

    def validate(self, attrs):
        # TODO: Move This To Permission
        pv = PV.check_user_access(self.context['request'].user, self.context['pv_id'])
        if pv is None:
            raise YouDontHaveAccessToThisPV
        return attrs

    def validate_reply_id(self, reply_id):
        # We Know Reply Message Exists Now Check Reply Is For This PV Or Not
        PVMessage.objects.get_or_raise(id=reply_id.id, pv_id=self.context['pv_id'])
        return reply_id

    def to_representation(self, instance):
        return {}
