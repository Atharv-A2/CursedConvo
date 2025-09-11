import json, os
import redis.asyncio as redis
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer

from dotenv import load_dotenv
load_dotenv()

REDIS_URL = os.environ.get("REDIS_URL")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.redis = redis_client
        self.room_name = "global_chat"
        self.room_group_name = f"chat_{self.room_name}"
        
        # Check if user is already online
        is_online = await self.redis.hexists("online_users", self.username)
        if is_online:
            await self.close(code=4000)
            return


        # Storing Timestamp
        login_timestamp = datetime.now().strftime("%m/%d/%y %I:%M %p")
        await self.redis.hset("online_users", self.username, login_timestamp)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.notify_online_users()

    async def disconnect(self, close_code):
        if hasattr(self, 'username') and self.scope.get("type") == "websocket":
            try:
                await self.redis.hdel("online_users", self.username)

                await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                )

                await self.notify_online_users()
            except Exception as e:
                print(f"[disconnect error] {e}")
            finally:
                await self.redis.close()

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
        users = await self.redis.hgetall("online_users")
        await self.channel_layer.group_send(
            "online_users_group",
            {
                "type": "update_online_users",
                "users": users
            }
        )

class OnlineUsersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.redis = redis_client
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
        await self.redis.close()

    async def send_online_users(self):
        users = await self.redis.hgetall("online_users")
        await self.send(text_data=json.dumps({
            "users": list(users)
        }))

    async def update_online_users(self, event):
        await self.send(text_data=json.dumps({
            "users": event["users"]
        }))