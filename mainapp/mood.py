from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import DailyMood
from .serializers import DailyMoodSerializer
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import Http404
from collections import Counter
import calendar
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_daily_mood(request):
    user = request.user  # Assuming authenticated user
    
    data = request.data.copy()
    data['user'] = user.id
    data['date'] = timezone.now().date()  # Set current date
    serializer = DailyMoodSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_weekly_mood_statistics(request):
    user = request.user  # Assuming authenticated user
    
    start_date = timezone.now().date() - timezone.timedelta(days=6)  # Last 7 days
    moods = DailyMood.objects.filter(user=user, date__gte=start_date).order_by('date')
    mood_data = DailyMoodSerializer(moods, many=True).data
    
    # Add day name based on date
    for item in mood_data:
        item_date = timezone.datetime.strptime(item['date'], '%Y-%m-%d').date()
        item['day'] = calendar.day_name[item_date.weekday()]
    
    mood_counts = dict(Counter([item['mood'] for item in mood_data]))
    
    # Prepare response with mood statistics, including day and date
    response_data = {
        'weekly_mood_data': mood_data,  # Includes day and date for each entry
        'weekly_mood_counts': mood_counts,
        'total_entries': sum(mood_counts.values()) if mood_counts else 0
    }
    return Response(response_data)