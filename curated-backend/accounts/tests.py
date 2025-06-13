from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core import mail

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_registration_flow(self):
        # Test registration
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify email was sent
        self.assertEqual(len(mail.outbox), 1)
        
        # Get OTP from email
        user = self.User.objects.get(email=self.user_data['email'])
        otp = user.otp
        
        # Verify OTP
        verify_response = self.client.post(reverse('verify-otp'), {
            'email': self.user_data['email'],
            'otp': otp
        })
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)
        
        # Try login after verification
        login_response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_response.data)

    # ...more test methods...
