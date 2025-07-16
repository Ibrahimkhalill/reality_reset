from django.urls import path
from . import views

urlpatterns = [
    path('challenges/', views.challenge_list_create, name='challenge-list'),
    path('challenges/<int:pk>/', views.challenge_detail, name='challenge-detail'),
    path('boost/<int:pk>/', views.challenge_read, name='challenge-read'),
    path('challenges/list/', views.challenge_list, name='challenge-list'),
]