import json, logging
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer

online_users = set()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']

        #handles the same username error
        if self.username in online_users:
            raise Exception("Retry with a New User\n")
        
        #Otherwise it adds the new user to the online_users set
        online_users.add(self.username)
        self.room_name = "global_chat"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.notify_online_users()

    
    async def disconnect(self, close_code):
        try:
            if hasattr(self, 'username') and self.username in online_users:
                online_users.discard(self.username)
                await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                )
                await self.notify_online_users()

        except AttributeError:
            logging.error("\nRefresh and Try Again with a New Username!!\n")

    async def receive(self, text_data):

        timestamp = datetime.now().strftime("%D %I:%M %p")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": text_data,
                "sender": self.username,
                "timestamp": timestamp,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "timestamp": event["timestamp"],
        }))

    async def notify_online_users(self):
        await self.channel_layer.group_send(
            "online_users_group",
            {
                "type": "update_online_users",
                "users": list(online_users)
            }
        )


class OnlineUsersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "online_users_group",
            self.channel_name
        )
        await self.accept()
        await self.send_online_users()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "online_users_group",
            self.channel_name
        )

    async def send_online_users(self):
        await self.send(text_data=json.dumps({
            "users": list(online_users)
        }))

    async def update_online_users(self, event):
        await self.send(text_data=json.dumps({
            "users": event["users"]
        }))