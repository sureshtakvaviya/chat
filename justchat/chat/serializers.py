from rest_framework import serializers 
 
from .models import Chat
class ChatSerializer(serializers.ModelSerializer): 
    # specify model and fields 
    class Meta: 
        model = Chat 
        fields = '__all__' 
  