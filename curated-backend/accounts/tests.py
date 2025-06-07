from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import CustomUser

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.token_url = reverse('token_obtain_pair')
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_user_registration_success(self):
        # Test successful registration
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email=self.user_data['email']).exists())
        self.assertFalse(CustomUser.objects.get(email=self.user_data['email']).is_active)  # User should be inactive until OTP verification

    def test_user_registration_invalid_data(self):
        # Test registration with invalid email
        invalid_data = self.user_data.copy()
        invalid_data['email'] = 'invalid-email'
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate_email(self):
        # First registration
        self.client.post(self.register_url, self.user_data)
        # Attempt duplicate registration
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)  # Update expected status code

    def test_token_obtain_with_valid_credentials(self):
        # Create active user and test token generation
        user = CustomUser.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            is_active=True
        )
        response = self.client.post(self.token_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_obtain_with_inactive_user(self):
        # Test token generation for inactive user
        user = CustomUser.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            is_active=False
        )
        response = self.client.post(self.token_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
