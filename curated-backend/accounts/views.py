from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
from .serializers import *
import random
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "message": "User registered successfully.",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def perform_create(self, serializer):
        user = serializer.save()
        otp = user.generate_otp()

        try:
            # Render email template
            html_message = render_to_string('email/auth/verify_email.html', {
                'otp': otp,
                'user': user
            })
            plain_message = strip_tags(html_message)

            # Send email
            send_mail(
                'Verify your CuratED account',
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            # Log error in production

        return user


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            if not user.is_active:
                return Response({
                    "error": "Please verify your email first",
                    "verification_required": True
                }, status=status.HTTP_403_FORBIDDEN)
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            })
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class ResendVerificationView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmailSerializer
    
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email, is_active=False)
            otp = user.generate_otp()  # Using the model method we defined
            
            send_mail(
                'Verify your CuratED account',
                f'Your new verification code is: {otp}\nThis code will expire in 10 minutes.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response({"message": "New verification code sent"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # For security, don't reveal whether the email exists
            return Response({"message": "If this email exists, a verification code has been sent."}, 
                          status=status.HTTP_200_OK)

class PasswordResetRequestView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmailSerializer
    
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"
            send_mail(
                'Reset your CuratED password',
                f'Click this link to reset your password: {reset_link}\nThis link will expire in 24 hours.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except User.DoesNotExist:
            pass  # Silently handle non-existent emails
        
        return Response({"message": "If this email exists, password reset instructions have been sent."}, 
                      status=status.HTTP_200_OK)

class PasswordResetConfirmView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            uid = urlsafe_base64_decode(serializer.validated_data['uid']).decode()
            user = User.objects.get(pk=uid)
            
            if default_token_generator.check_token(user, serializer.validated_data['token']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({"error": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)
            
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

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
            if user.is_active:
                return Response({"message": "Account already verified"}, status=status.HTTP_200_OK)
            
            # Debug line to check values
            print(f"Received OTP: {otp}, Stored OTP: {user.otp}")
            
            # Convert both to strings for comparison
            if str(user.otp) != str(otp):
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check expiration
            if not user.otp_created or now() - user.otp_created > timedelta(minutes=10):
                return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)
            
            user.is_active = True
            user.otp = None
            user.otp_created = None
            user.save()
            
            # Generate tokens after verification
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Account verified successfully",
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        # Check for remember_me flag
        remember_me = request.data.get('remember_me', False)
        
        if remember_me:
            # Get the refresh token
            refresh = RefreshToken(response.data['refresh'])
            
            # Update its lifetime
            refresh.set_exp(lifetime=timedelta(days=30))
            
            # Update response with new tokens
            response.data['refresh'] = str(refresh)
            response.data['access'] = str(refresh.access_token)
            
            # Set refresh token in HTTP-only cookie
            response.set_cookie(
                'refresh_token',
                response.data['refresh'],
                max_age=30 * 24 * 60 * 60,  # 30 days
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Strict'
            )
        
        return response
