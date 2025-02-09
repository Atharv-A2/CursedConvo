from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<username>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/online/$', consumers.OnlineUsersConsumer.as_asgi()),
]