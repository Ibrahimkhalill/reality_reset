from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Chat, ChatMessage
from .serializers import ChatMessageSerializer, ChatSerializer, ChatTitleSerializer
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import Http404
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_new_chat(request):
    user = request.user
    chat = Chat.objects.create(user=user)
    serializer = ChatSerializer(chat)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    user = request.user
    content = request.data.get('content', '').strip()
    chat_id = request.data.get('chat_id')

    if not content :
        return Response({"error": "content is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not chat_id:
        # Create new chat with title as first 20 characters of content
        chat = Chat.objects.create(user=user, title=content[:20])
        chat_id = chat.id
    else:
        try:
            chat = Chat.objects.get(pk=chat_id, user=user)
        except Chat.DoesNotExist:
            raise Http404

    # User message
    user_message_data = {
        'chat': chat_id,
        'sender': user.id,
        'is_bot': False,
        'content': content
    }
    user_serializer = ChatMessageSerializer(data=user_message_data)
    if user_serializer.is_valid():
        user_message = user_serializer.save()

    # Bot response (simple logic)
    bot_response = generate_bot_response(content)
    bot_message_data = {
        'chat': chat_id,
        'is_bot': True,
        'content': bot_response
    }
    bot_serializer = ChatMessageSerializer(data=bot_message_data)
    if bot_serializer.is_valid():
        bot_serializer.save()

    chat_history = Chat.objects.get(pk=chat_id)
    serializer = ChatSerializer(chat_history)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_history(request, chat_id):
    user = request.user
    try:
        chat = Chat.objects.get(pk=chat_id, user=user)
        serializer = ChatMessageSerializer(chat)
        return Response(serializer.data)
    except Chat.DoesNotExist:
        raise Http404



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat(request):
    user = request.user
    try:
        chat = Chat.objects.filter(user=user)
        serializer = ChatTitleSerializer(chat, many=True)
        return Response(serializer.data)
    except Chat.DoesNotExist:
        raise Http404


# Simple bot response logic (can be expanded)
def generate_bot_response(user_input):
    user_input = user_input.lower()
    if "sad" in user_input or "down" in user_input:
        return "I'm sorry to hear that. Would you like some encouragement?"
    elif "studied" in user_input or "hard" in user_input:
        return "Great effort! Keep it up!"
    else:
        return "Thanks for sharing. How can I assist you today?"