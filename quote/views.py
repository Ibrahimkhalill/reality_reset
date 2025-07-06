from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Quote
from .serializers import QuoteSerializer
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])  # ✅ use brackets
def quote_list_create(request):
    if request.method == 'GET':
        quotes = Quote.objects.all()
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = QuoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])  # ✅ use brackets
def quote_list(request):
    if request.method == 'GET':
        quotes = Quote.objects.all().order_by('-created_at')  # 🔁 recent first
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)
    
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])  # ✅ use brackets
def quote_detail(request, pk):
    try:
        quote = Quote.objects.get(pk=pk)
    except Quote.DoesNotExist:
        return Response({"error": "Quote not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = QuoteSerializer(quote)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = QuoteSerializer(quote, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        quote.delete()
        return Response({"message": "Quote deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
