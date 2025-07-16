
from django.urls import path 
from .views import *
from .feeling import *
from .mood import *

urlpatterns = [

  path("get/all-data/dashboard/",dashboard_view),
  path('terms/', terms_list_create, name='terms-list'),
  path('terms/<int:pk>/', terms_detail, name='terms-detail'),

  #feeling api

   path('save-feeling/', save_daily_feeling, name='save-feeling'),
   path('weekly-history/', get_weekly_history, name='weekly-history'),

   #mood api

    path('save-mood/', save_daily_mood, name='save-mood'),
    path('weekly-mood-stats/', get_weekly_mood_statistics, name='weekly-mood-stats'),
  
]
