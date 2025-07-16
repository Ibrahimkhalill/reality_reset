from django.urls import path
from . import views

urlpatterns = [
    path('new-chat/', views.create_new_chat, name='new-chat'),
    path('send-message/', views.send_message, name='send-message'),
    path('chat-history/<uuid:chat_id>/', views.get_chat_history, name='chat-history'),
    path('chat-history/all/', views.get_chat, name='chat-all'),
]