import json
from .models import Chat
from .serializers import ChatSerializer
from django.http import QueryDict
from django.contrib.auth.models import User
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        chat=Chat.objects.filter(roomname=self.room_group_name)
        context={
            'old_chat':self.messages_to_json(chat)
        }
        print(context)
        self.send(text_data=json.dumps(context))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    def messages_to_json(self,messages):
        result=[]
        for message in messages:
            result.append(self.message_to_json(message))
        return(result)
    def message_to_json(self,messages):
        return{
            'author':messages.author.username,
            'content':messages.content,
            'timestamp':str(messages.timestamp)
        }

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        query_dict = QueryDict('', mutable=True)
        message = text_data_json['message']
        user=str(self.scope["user"])
        query_dict['author']=User.objects.get(username=user).id
        query_dict['roomname']=self.room_group_name
        query_dict['content']=message
        serializer=ChatSerializer(data=query_dict)
        serializer.is_valid()
        if serializer.is_valid():
            print(type(query_dict))
            serializer.save()
        #Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user':user
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user=event['user']
        print(message)
        # Send message to WebSocket
        self.send(
            text_data=json.dumps({
            'user':user,
            'message': message
        }))
