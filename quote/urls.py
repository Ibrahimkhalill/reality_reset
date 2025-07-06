from django.urls import path
from . import views

urlpatterns = [
    path('quotes/', views.quote_list_create, name='quote-list'),
    path('quote-list/', views.quote_list, name='quote-list'),
    path('quotes/<int:pk>/', views.quote_detail, name='quote-detail'),
]