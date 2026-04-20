from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users_app.models import CustomUser


class RegistrationTest(APITestCase):

    def setUp(self):
        self.url = reverse('registration')
        self.valid_data = {
            'username': 'testuser',
            'email': 'test@mail.de',
            'password': 'testpass123',
            'repeated_password': 'testpass123',
            'type': 'customer'
        }

    def test_registration_success(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertIn('token', response.data)

    def test_registration_password_mismatch(self):
        self.valid_data['repeated_password'] = 'wrongpassword'
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_missing_fields(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_duplicate_username(self):
        self.client.post(self.url, self.valid_data)
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTest(APITestCase):

    def setUp(self):
        self.url = reverse('login')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@mail.de',
            password='testpass123',
            profile_type='customer'
        )

    def test_login_success(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('user_id', response.data)

    def test_login_wrong_password(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent_user(self):
        response = self.client.post(self.url, {
            'username': 'niemand',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
