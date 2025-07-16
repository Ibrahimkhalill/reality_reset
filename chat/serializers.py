from rest_framework import serializers
from .models import Chat, ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'chat', 'sender', 'is_bot', 'content', 'date']

class ChatSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'user', 'title', 'created_at', 'messages']


class ChatTitleSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Chat
        fields = ['id', 'user', 'title']