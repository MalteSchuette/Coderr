from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users_app.models import CustomUser
from offers_app.models import Offer, OfferDetail


class OfferTest(APITestCase):

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
        self.valid_offer_data = {
            'title': 'Test Offer',
            'description': 'Test Description',
            'details': [
                {
                    'title': 'Basic',
                    'revisions': 2,
                    'delivery_time_in_days': 5,
                    'price': 100,
                    'features': ['Logo Design'],
                    'offer_type': 'basic'
                },
                {
                    'title': 'Standard',
                    'revisions': 5,
                    'delivery_time_in_days': 7,
                    'price': 200,
                    'features': ['Logo Design', 'Visitenkarte'],
                    'offer_type': 'standard'
                },
                {
                    'title': 'Premium',
                    'revisions': 10,
                    'delivery_time_in_days': 10,
                    'price': 500,
                    'features': ['Logo Design', 'Visitenkarte', 'Flyer'],
                    'offer_type': 'premium'
                }
            ]
        }
        self.list_url = reverse('offer-list-create')

    def test_get_offer_list_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_offer_as_business_user(self):
        self.client.force_authenticate(user=self.business_user)
        response = self.client.post(
            self.list_url,
            self.valid_offer_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 1)
        self.assertEqual(OfferDetail.objects.count(), 3)

    def test_create_offer_as_customer_user(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.post(
            self.list_url,
            self.valid_offer_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_offer_unauthenticated(self):
        response = self.client.post(
            self.list_url,
            self.valid_offer_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_offer_with_less_than_3_details(self):
        self.client.force_authenticate(user=self.business_user)
        invalid_data = self.valid_offer_data.copy()
        invalid_data['details'] = self.valid_offer_data['details'][:2]
        response = self.client.post(
            self.list_url,
            invalid_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OfferDetailTest(APITestCase):

    def setUp(self):
        self.business_user = CustomUser.objects.create_user(
            username='business_user',
            email='business@mail.de',
            password='testpass123',
            profile_type='business'
        )
        self.other_business_user = CustomUser.objects.create_user(
            username='other_business',
            email='other@mail.de',
            password='testpass123',
            profile_type='business'
        )
        self.offer = Offer.objects.create(
            user=self.business_user,
            title='Test Offer',
            description='Test'
        )
        self.detail = OfferDetail.objects.create(
            offer=self.offer,
            title='Basic',
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            offer_type='basic'
        )
        self.detail_url = reverse(
            'offerdetail-detail', kwargs={'pk': self.detail.pk})
        self.offer_url = reverse('offer-detail', kwargs={'pk': self.offer.pk})

    def test_get_offer_detail(self):
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get(self.offer_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('details', response.data)

    def test_patch_offer_as_owner(self):
        self.client.force_authenticate(user=self.business_user)
        response = self.client.patch(
            self.offer_url,
            {'title': 'Updated Title'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_patch_offer_as_other_user(self):
        self.client.force_authenticate(user=self.other_business_user)
        response = self.client.patch(
            self.offer_url,
            {'title': 'Hacked Title'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_offer_as_owner(self):
        self.client.force_authenticate(user=self.business_user)
        response = self.client.delete(self.offer_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Offer.objects.count(), 0)

    def test_delete_offer_as_other_user(self):
        self.client.force_authenticate(user=self.other_business_user)
        response = self.client.delete(self.offer_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
