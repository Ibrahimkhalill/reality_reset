from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Challenge
from .serializers import ChallengeSerializer
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])  # ✅ use bracket
def challenge_list_create(request):
    if request.method == 'GET':
        challenges = Challenge.objects.all()
        serializer = ChallengeSerializer(challenges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ChallengeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT','DELETE'])
@permission_classes([IsAdminUser])  # ✅ use bracket
def challenge_detail(request, pk):
    try:
        challenge = Challenge.objects.get(pk=pk)
    except Challenge.DoesNotExist:
        raise Http404
    if request.method == 'GET':
        serializer = ChallengeSerializer(challenge)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ChallengeSerializer(challenge, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        challenge.delete()
        return Response({"message": "Challenges deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # ✅ use bracket
def challenge_list(request):
    if request.method == 'GET':
        challenges = Challenge.objects.all().order_by('-created_at')
        serializer = ChallengeSerializer(challenges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
  


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def challenge_read(request, pk):
    try:
        challenge = Challenge.objects.get(pk=pk)
        challenge.is_read = True
        challenge.save()
        serializer = ChallengeSerializer(challenge)
        return Response({"message": "Read successfully done", "data": serializer.data}, status=status.HTTP_200_OK)
    except Challenge.DoesNotExist:
        raise Http404
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
   
    
       
 