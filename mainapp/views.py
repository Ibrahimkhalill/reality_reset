from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from quote.models import Quote
from boost.models import Challenge
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TermsAndConditions
from .serializers import TermsAndConditionsSerializer
from django.http import Http404


User = get_user_model()

@api_view(['GET'])
def dashboard_view(request):
    total_users = User.objects.filter(is_staff=False).count()
    total_quotes = Quote.objects.count()
    total_challenges = Challenge.objects.count()
    total_active_users = User.objects.filter(is_staff=False, is_active=True, is_verified= True).count()
    
    dashboard_data = {
        'total_users': total_users,
        'total_quotes': total_quotes,
        'total_challenges': total_challenges,
        'total_active_users': total_active_users
    }
    return Response(dashboard_data)





@api_view(['GET', 'POST'])
def terms_list_create(request):
    if request.method == 'GET':
        terms = TermsAndConditions.objects.all().first()
        serializer = TermsAndConditionsSerializer(terms)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TermsAndConditionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def terms_detail(request, pk):
    try:
        terms = TermsAndConditions.objects.get(pk=pk)
    except TermsAndConditions.DoesNotExist:
        raise Http404
    if request.method == 'GET':
        serializer = TermsAndConditionsSerializer(terms)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TermsAndConditionsSerializer(terms, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        terms.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



