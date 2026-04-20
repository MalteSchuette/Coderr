from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users_app.models import CustomUser


class ProfileTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@mail.de',
            password='testpass123',
            profile_type='customer'
        )
        self.other_user = CustomUser.objects.create_user(
            username='otheruser',
            email='other@mail.de',
            password='testpass123',
            profile_type='customer'
        )
        self.url = reverse('profile-detail', kwargs={'pk': self.user.pk})

    def test_get_profile_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data)
        self.assertIn('type', response.data)

    def test_get_profile_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_profile_as_owner(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, {'first_name': 'Max'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Max')

    def test_patch_profile_as_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(self.url, {'first_name': 'Hacker'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_profile_unauthenticated(self):
        response = self.client.patch(self.url, {'first_name': 'Hacker'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_business_profiles(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('business-profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_customer_profiles(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('customer-profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
