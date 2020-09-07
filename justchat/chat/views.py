from django.shortcuts import render
from django.contrib.auth import decorators
from django.http import HttpResponse
from .models import Chat


def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    print(Chat.objects.all())
    return render(request, 'chat/room.html',{'room_name': room_name}) 