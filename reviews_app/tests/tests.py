from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users_app.models import CustomUser
from reviews_app.models import Review


class ReviewTest(APITestCase):

    def setUp(self):
        self.business_user = CustomUser.objects.create_user(
            username='business_user',
            email='business@mail.de',
            password='testpass123',
            profile_type='business'
        )
        self.customer_user = CustomUser.objects.create_user(
            username='customer_user',
            email='customer@mail.de',
            password='testpass123',
            profile_type='customer'
        )
        self.other_customer = CustomUser.objects.create_user(
            username='other_customer',
            email='other@mail.de',
            password='testpass123',
            profile_type='customer'
        )
        self.list_url = reverse('review-list-create')
        self.valid_data = {
            'business_user': self.business_user.pk,
            'rating': 4,
            'description': 'Sehr guter Service!'
        }

    def test_create_review_as_customer(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.post(self.list_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

    def test_create_review_as_business_user(self):
        self.client.force_authenticate(user=self.business_user)
        response = self.client.post(self.list_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_review_unauthenticated(self):
        response = self.client.post(self.list_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_duplicate_review(self):
        self.client.force_authenticate(user=self.customer_user)
        self.client.post(self.list_url, self.valid_data)
        response = self.client.post(self.list_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_review_list_authenticated(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_review_list_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReviewUpdateDeleteTest(APITestCase):

    def setUp(self):
        self.business_user = CustomUser.objects.create_user(
            username='business_user',
            email='business@mail.de',
            password='testpass123',
            profile_type='business'
        )
        self.customer_user = CustomUser.objects.create_user(
            username='customer_user',
            email='customer@mail.de',
            password='testpass123',
            profile_type='customer'
        )
        self.other_customer = CustomUser.objects.create_user(
            username='other_customer',
            email='other@mail.de',
            password='testpass123',
            profile_type='customer'
        )
        self.review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description='Sehr guter Service!'
        )
        self.detail_url = reverse(
            'review-detail', kwargs={'pk': self.review.pk})

    def test_patch_review_as_reviewer(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.patch(self.detail_url, {'rating': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 5)

    def test_patch_review_as_other_customer(self):
        self.client.force_authenticate(user=self.other_customer)
        response = self.client.patch(self.detail_url, {'rating': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_review_unauthenticated(self):
        response = self.client.patch(self.detail_url, {'rating': 1})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_review_as_reviewer(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)

    def test_delete_review_as_other_customer(self):
        self.client.force_authenticate(user=self.other_customer)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
