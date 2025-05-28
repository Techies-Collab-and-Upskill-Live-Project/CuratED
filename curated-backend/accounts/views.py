from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import random
from django.core.mail import sendmail
from .serializers import *

User = get_user_model()


class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.is_active:
                return Response({"error": "Email is already registered and verified."}, status=status.HTTP_409_CONFLICT)
            else:
                return Response({"error": "Email is already registered but not verified. Please check your email for the OTP or request a new one."}, status=status.HTTP_409_CONFLICT)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.otp_created = now()
        user.save()

        # Send OTP via email
        try:
            send_mail(
                'Your OTP Code',
                f'Your OTP is: {otp}',
                'noreply@example.com',
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({"error": "Failed to send OTP email. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "message": "User registered successfully. OTP sent to email.",
            "user": serializer.data
        }, status=status.HTTP_201_CREATED)
        

class OTPVerifyView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OTPVerifySerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        if user.is_active:
            return Response({"message": "Account already verified."}, status=status.HTTP_200_OK)
        if user.otp != otp:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        if not user.otp_created or now() - user.otp_created > timedelta(minutes=10):
            return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active=True
        user.otp = None
        user.otp_created = None
        user.save()
        
        return Response({"message": "Account verified successfully."}, status=status.HTTP_200_OK)