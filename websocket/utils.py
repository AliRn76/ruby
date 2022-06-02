from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_message_in_ws(user_channel_name: str, message: dict):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(
        user_channel_name, {
            'type': 'send_message',
            'text': message
        }
    )
