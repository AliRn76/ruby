from django.db.models.signals import post_save
from django.dispatch import receiver

from cache.queries import is_online, save_unread_message
from user.models import UserRoom
from websocket.utils import send_message_in_ws
from pv.utils import get_pv_members
from pv.models import PVMessage, PV


@receiver(post_save, sender=PVMessage)
def send_pv_message(sender, instance=None, created=False, **kwargs):
    if created:
        users = get_pv_members(instance.pv_id.id)
        for user_id in users:
            if user_channel_name := is_online(user_id):
                send_message_in_ws(user_channel_name, instance.dict())
            else:
                save_unread_message(user_id, instance.dict())


@receiver(post_save, sender=PVMessage)
def update_pv_user_rooms(sender, instance=None, created=False, **kwargs):
    if created:  # user_id=instance.user_id.id,
        rooms = UserRoom.objects.filter(is_pv=True, room_id=instance.pv_id.id)
        for room in rooms:
            is_from_me = bool(room.user_id == instance.user_id)
            if instance.text is None:
                room.update_last_message('|-Image-|', is_from_me=is_from_me)
            else:
                room.update_last_message(instance.text, is_from_me=is_from_me)


@receiver(post_save, sender=PV)
def add_pv_to_user_rooms(sender, instance=None, created=False, **kwargs):
    if created:
        UserRoom.objects.create(is_pv=True, room_id=instance.id, user_id=instance.user1_id,
                                avatar=instance.user2_id.profile_picture, name=instance.user2_id.full_name)
        UserRoom.objects.create(is_pv=True, room_id=instance.id, user_id=instance.user2_id,
                                avatar=instance.user1_id.profile_picture, name=instance.user1_id.full_name)
