import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from cache.queries import get_unread_messages_from_redis, set_user_offline_in_redis, set_user_online_in_redis


class WSStatus:
    UNAUTHORIZED = 3001


class RubyConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        await self.accept()
        # 1. Authentication
        if self.user is None:
            return await self.close(code=WSStatus.UNAUTHORIZED)
        # 2. Update LastLogin & IsOnline
        await self.update_last_login()
        await self.set_user_online()
        # 3. Check It Has Unreceived Message ?
        for message in await self.get_unreceived_messages():
            # 4. Send His Notifications If Not None
            await self.send(text_data=message)

    async def send_message(self, message):
        print(f'[send_message] --> {message["text"]}')
        await self.send(text_data=await self.encode_json(message['text']))

    async def disconnect(self, code):
        print(f'[Disconnect] --> {self.user} - Code: {code}')
        await self.set_user_offline()

    # # # Class Methods

    @classmethod
    async def decode_json(cls, text_data: str):
        return json.loads(text_data)

    @classmethod
    async def encode_json(cls, content):
        return json.dumps(content)

    # # # Methods

    @database_sync_to_async
    def update_last_login(self):
        self.user.update_last_login()

    @database_sync_to_async
    def set_user_online(self):
        set_user_online_in_redis(self.user.id, self.channel_name)

    @database_sync_to_async
    def set_user_offline(self):
        set_user_offline_in_redis(self.user.id)

    @database_sync_to_async
    def get_unreceived_messages(self):
        # TODO: Make it task , if it was 1000 mess  age send them 20 message every 2 sec
        return get_unread_messages_from_redis(self.user.id)
