from django.urls import path, include
from accounts.views import (
    RegisterView, OTPVerifyView, ResendVerificationView,
    PasswordResetRequestView, PasswordResetConfirmView, ChangePasswordView
)
from rest_framework_simplejwt.views import TokenObtainPairView
from django.test import TestCase
from django.urls import reverse, resolve, NoReverseMatch

# Define URLs for testing only
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    path('resend-verification/', ResendVerificationView.as_view(), name='resend-verification'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password/change/', ChangePasswordView.as_view(), name='password-change'),
    # Add other URL patterns as needed for testing
]

class URLPatternTests(TestCase):
    """Test to discover actual URL names in the project"""
    
    def test_discover_url_names(self):
        """Print available URL names to help debug test failures"""
        # List of URL name patterns to try
        patterns_to_try = [
            'youtube-search', 'search', 'search-youtube',
            'watched-videos', 'watched', 'history',
            'playlist-list', 'playlist-items', 'playlists'
        ]
        
        for pattern in patterns_to_try:
            try:
                url = reverse(pattern)
                print(f"URL name '{pattern}' resolves to: {url}")
            except NoReverseMatch:
                print(f"URL name '{pattern}' is not available")
