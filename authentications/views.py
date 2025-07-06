from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import OTP, UserProfile , CustomUser
from .serializers import (
    CustomUserSerializer,
    CustomUserCreateSerializer,
    UserProfileSerializer,
    OTPSerializer,
    LoginSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from reality_reset.utils import error_response
import random

def generate_otp():
    return str(random.randint(1000, 9999))

User = get_user_model()

def send_otp_email(email, otp):
    html_content = render_to_string('otp_email_template.html', {'otp': otp, 'email': email})
    msg = EmailMultiAlternatives(
        subject='Your OTP Code',
        body=f'Your OTP is {otp}',
        from_email='hijabpoint374@gmail.com',
        to=[email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = CustomUserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Send OTP for verification
        otp = generate_otp()
        otp_data = {'email': user.email, 'otp': otp}
        otp_serializer = OTPSerializer(data=otp_data)
        if otp_serializer.is_valid():
            otp_serializer.save()
            try:
                send_otp_email(email=user.email, otp=otp)
            except Exception as e:
                return error_response(
                    code=500,
                    message="Failed to send OTP email",
                    details={"error": [str(e)]}
                )
        return Response({
            "message": "User registered. Please verify your email with the OTP sent",
            "user": serializer.data
        }, status=status.HTTP_201_CREATED)
    return error_response(code=400, details=serializer.errors)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        try:
            is_verified = user.is_verified
            profile = user.user_profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user, name=user.email.split('@')[0])
        profile_serializer = UserProfileSerializer(profile)
        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "role": user.role,
            "is_verified" : is_verified,
            "profile": profile_serializer.data
        }, status=status.HTTP_200_OK)
    return error_response(code=401, details=serializer.errors)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_users(request):
    users = User.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    try:
        profile = request.user.user_profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, name=request.user.email.split('@')[0])

    if request.method == 'GET':
        user = CustomUser.objects.get(id=request.user.id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return error_response(code=400, details=serializer.errors)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_otp(request):
    email = request.data.get('email')
    if not email:
        return error_response(
            code=400,
            details={"email": ["This field is required"]}
        )
    
    try:
        user = User.objects.get(email=email)
        if user.is_verified:
            return error_response(
                code=400,
                details={"email": ["This account is already verified"]}
            )
    except User.DoesNotExist:
        return error_response(
            code=404,
            details={"email": ["No user exists with this email"]}
        )
    
    otp = generate_otp()
    otp_data = {'email': email, 'otp': otp}
    OTP.objects.filter(email=email).delete()
    serializer = OTPSerializer(data=otp_data)
    if serializer.is_valid():
        serializer.save()
        try:
            send_otp_email(email=email, otp=otp)
        except Exception as e:
            return error_response(
                code=500,
                message="Failed to send OTP email",
                details={"error": [str(e)]}
            )
        return Response({"message": "OTP sent to your email"}, status=status.HTTP_201_CREATED)
    return error_response(code=400, details=serializer.errors)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp_reset(request):
    email = request.data.get('email')
    otp_value = request.data.get('otp')
    
    if not email or not otp_value:
        details = {}
        if not email:
            details["email"] = ["This field is required"]
        if not otp_value:
            details["otp"] = ["This field is required"]
        return error_response(code=400, details=details)
    
    try:
        otp_obj = OTP.objects.get(email=email)
        if otp_obj.otp != otp_value:
            return error_response(
                code=400,
                details={"otp": ["The provided OTP is invalid"]}
            )
        if otp_obj.is_expired():
            return error_response(
                code=400,
                details={"otp": ["The OTP has expired"]}
            )
        return Response({"message": "OTP verified successfully"})
    except OTP.DoesNotExist:
        return error_response(
            code=404,
            details={"email": ["No OTP found for this email"]})

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserProfileSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    email = request.data.get('email')
    otp_value = request.data.get('otp')
    
    if not email or not otp_value:
        details = {}
        if not email:
            details["email"] = ["This field is required"]
        if not otp_value:
            details["otp"] = ["This field is required"]
        return error_response(code=400, details=details)
    
    try:
        otp_obj = OTP.objects.get(email=email)
        if otp_obj.otp != otp_value:
            return error_response(
                code=400,
                details={"otp": ["The provided OTP is invalid"]}
            )
        if otp_obj.is_expired():
            return error_response(
                code=400,
                details={"otp": ["The OTP has expired"]}
            )
        
        # Verify the user
        try:
            user = User.objects.get(email=email)
            if user.is_verified:
                return error_response(
                    code=400,
                    details={"email": ["This account is already verified"]}
                )
            
            user.is_verified = True
            user.save()
            otp_obj.delete()
            
            # ✅ Generate tokens
            refresh = RefreshToken.for_user(user)

            # ✅ Create profile if not exists
            try:
                profile = user.user_profile
            except UserProfile.DoesNotExist:
                profile = UserProfile.objects.create(user=user, name=user.email.split('@')[0])

            profile_serializer = UserProfileSerializer(profile)

            return Response({
                "message": "Email verified successfully.",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "role": user.role,
                "is_verified": user.is_verified,
                "profile": profile_serializer.data
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return error_response(
                code=404,
                details={"email": ["No user exists with this email"]}
            )

    except OTP.DoesNotExist:
        return error_response(
            code=404,
            details={"email": ["No OTP found for this email"]}
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    email = request.data.get('email')
    if not email:
        return error_response(
            code=400,
            details={"email": ["This field is required"]}
        )
    
    try:
        user = User.objects.get(email=email)
        if not user.is_verified:
            return error_response(
                code=400,
                details={"email": ["Please verify your email before resetting your password"]}
            )
    except User.DoesNotExist:
        return error_response(
            code=404,
            details={"email": ["No user exists with this email"]}
        )

    otp = generate_otp()
    otp_data = {'email': email, 'otp': otp}
    OTP.objects.filter(email=email).delete()
    serializer = OTPSerializer(data=otp_data)
    if serializer.is_valid():
        serializer.save()
        try:
            send_otp_email(email=email, otp=otp)
        except Exception as e:
            return error_response(
                code=500,
                message="Failed to send OTP email",
                details={"error": [str(e)]}
            )
        return Response({"message": "OTP sent to your email"}, status=status.HTTP_201_CREATED)
    return error_response(code=400, details=serializer.errors)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    email = request.data.get('email')
    otp_value = request.data.get('otp')
    new_password = request.data.get('new_password')

    if not all([email, otp_value, new_password]):
        details = {}
        if not email:
            details["email"] = ["This field is required"]
        if not otp_value:
            details["otp"] = ["This field is required"]
        if not new_password:
            details["new_password"] = ["This field is required"]
        return error_response(code=400, details=details)

    try:
        otp_obj = OTP.objects.get(email=email)
        if otp_obj.otp != otp_value:
            return error_response(
                code=400,
                details={"otp": ["The provided OTP is invalid"]}
            )
        if otp_obj.is_expired():
            return error_response(
                code=400,
                details={"otp": ["The OTP has expired"]}
            )

        user = User.objects.get(email=email)
        if not user.is_verified:
            return error_response(
                code=400,
                details={"email": ["Please verify your email before resetting your password"]}
            )
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return error_response(
                code=400,
                details={"new_password": e.messages}
            )

        user.set_password(new_password)
        user.save()
        otp_obj.delete()
        return Response({'message': 'Password reset successful'})
    except OTP.DoesNotExist:
        return error_response(
            code=404,
            details={"email": ["No OTP found for this email"]}
        )
    except User.DoesNotExist:
        return error_response(
            code=404,
            details={"email": ["No user exists with this email"]}
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')

    if not current_password or not new_password:
        details = {}
        if not current_password:
            details["current_password"] = ["This field is required"]
        if not new_password:
            details["new_password"] = ["This field is required"]
        return error_response(code=400, details=details)

    user = request.user
    if not user.check_password(current_password):
        return error_response(
            code=400,
            details={"current_password": ["The current password is incorrect"]}
        )

    try:
        validate_password(new_password, user)
    except ValidationError as e:
        return error_response(
            code=400,
            details={"new_password": e.messages}
        )

    user.set_password(new_password)
    user.save()
    return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)




@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if user.is_superuser:
            return Response({"error": "Cannot delete a superuser."}, status=status.HTTP_403_FORBIDDEN)
        
        user.delete()
        return Response({"message": f"User ID {user_id} deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)