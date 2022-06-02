from django.db.models.signals import post_save
from django.dispatch import receiver

from cache.queries import is_online, save_unread_message
from websocket.utils import send_message_in_ws
from pv.utils import get_pv_members
from pv.models import PVMessage


@receiver(post_save, sender=PVMessage)
def send_pv_message(sender, instance=None, created=False, **kwargs):
    if created:
        users = get_pv_members(instance.pv_id.id)
        for user_id in users:
            if user_channel_name := is_online(user_id):
                send_message_in_ws(user_channel_name, instance.dict())
            else:
                save_unread_message(user_id, instance.dict())
