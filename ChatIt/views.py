from django.shortcuts import render

def chat_room(request, username):
    return render(request, "chat/chat_room.html", {"username" : username})

def online_users_view(request):
    return render(request, "chat/online_users.html")