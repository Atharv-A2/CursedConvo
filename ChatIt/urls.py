from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:username>/', views.chat_room, name='chat_room'),
    path('online/', views.online_users_view, name='online_users'),
]