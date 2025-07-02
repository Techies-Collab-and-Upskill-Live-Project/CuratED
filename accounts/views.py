from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, serializers
import logging
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
from .serializers import *
from django.template.loader import render_to_string
from django.utils import timezone
import random
import secrets
from django.core.mail import send_mail

User = get_user_model()
logger = logging.getLogger(__name__)

class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data.get('email')
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            if existing_user.is_active:
                raise serializers.ValidationError({"error": "Email is already registered and verified."})
            raise serializers.ValidationError({"error": "Email is already registered but not verified. Please check your email for the OTP or request a new one."})

        user = serializer.save()
        user.is_active = False
        
        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.otp_created = now()
        user.save()

        subject = "Your CuratED OTP Verification Code"
        html_message = render_to_string('email/auth/verify_email.html', {'otp': otp, 'email': email})
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
        
        try:
            send_mail(
                subject,
                '',
                from_email,
                [email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"OTP email sent to {email}")
        except Exception as e:
            logger.error(f"Error sending OTP email to {email}: {str(e)}")

        return Response(
            {'message': 'User registered. OTP sent to your email.', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )

class ResendVerificationView(CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'Email is required.'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=404)

        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.otp_created = now()  # Fixed field name to match model
        user.save()

        subject = "Your CuratED OTP Verification Code"
        html_message = render_to_string('email/auth/verify_email.html', {'otp': otp, 'email': email})
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)

        try:
            send_mail(
                subject,
                '',
                from_email,
                [email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Resent OTP email to {email}")
        except Exception as e:
            logger.error(f"Error resending OTP email to {email}: {str(e)}")

        return Response({'detail': 'OTP resent to your email.'}, status=200)

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

            subject = "Password Reset Request"
            html_message = render_to_string('email/auth/password_reset.html', {'reset_link': reset_link, 'email': email})
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)

            send_mail(
                subject,
                '',
                from_email,
                [email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Password reset link sent to {email}")

        except User.DoesNotExist:
            pass
        except Exception as e:
            logger.error(f"Error sending password reset email to {email}: {str(e)}")

        return Response(
            {"message": "If this email exists, password reset instructions have been sent via email."},
            status=200
        )

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
            if user.otp != otp:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            if not user.otp_created or now() - user.otp_created > timedelta(minutes=10):
                return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)
            
            user.is_active = True
            user.otp = None
            user.otp_created = None
            user.save()
            return Response({"message": "Account verified successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            user = User.objects.get(email=email)
            if user.is_active:
                return Response({"message": "Account already verified"}, status=status.HTTP_200_OK)
            
            if user.otp != otp:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not user.otp_created or now() - user.otp_created > timedelta(minutes=10):
                return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)
            
            user.is_active = True
            user.otp = None
            user.otp_created = None
            user.save()
            
            return Response({"message": "Account verified successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
