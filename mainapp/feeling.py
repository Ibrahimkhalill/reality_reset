from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DailyFeeling
from .serializers import DailyFeelingSerializer
from django.utils import timezone
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
import calendar


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_daily_feeling(request):
    user = request.user  # Assuming authenticated user

    data = request.data.copy()
    data['user'] = user.id
    data['date'] = timezone.now().date()  # Set current date
    serializer = DailyFeelingSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_weekly_history(request):
    user = request.user  # Assuming authenticated user
  
    
    start_date = timezone.now().date() - timezone.timedelta(days=6)  # Last 7 days
    feelings = DailyFeeling.objects.filter(user=user, date__gte=start_date).order_by('date')
    serializer = DailyFeelingSerializer(feelings, many=True)
    
    # Add day name based on date
    for item in serializer.data:
        item_date = timezone.datetime.strptime(item['date'], '%Y-%m-%d').date()
        item['day'] = calendar.day_name[item_date.weekday()]
    
    return Response(serializer.data, status=status.HTTP_200_OK)