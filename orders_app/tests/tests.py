from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users_app.models import CustomUser
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


class OrderTest(APITestCase):

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
        self.admin_user = CustomUser.objects.create_user(
            username='admin_user',
            email='admin@mail.de',
            password='testpass123',
            is_staff=True
        )
        self.offer = Offer.objects.create(
            user=self.business_user,
            title='Test Offer',
            description='Test'
        )
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title='Basic',
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            offer_type='basic'
        )
        self.list_url = reverse('order-list-create')

    def test_create_order_as_customer(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.post(self.list_url, {
            'offer_detail_id': self.offer_detail.pk
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(response.data['title'], 'Basic')
        self.assertEqual(response.data['price'], 100)

    def test_create_order_as_business_user(self):
        self.client.force_authenticate(user=self.business_user)
        response = self.client.post(self.list_url, {
            'offer_detail_id': self.offer_detail.pk
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_order_unauthenticated(self):
        response = self.client.post(self.list_url, {
            'offer_detail_id': self.offer_detail.pk
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_order_list_authenticated(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order_list_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderUpdateDeleteTest(APITestCase):

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
        self.admin_user = CustomUser.objects.create_user(
            username='admin_user',
            email='admin@mail.de',
            password='testpass123',
            is_staff=True
        )
        self.offer = Offer.objects.create(
            user=self.business_user,
            title='Test Offer',
            description='Test'
        )
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title='Basic',
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            offer_type='basic'
        )
        # Order direkt in DB erstellen
        self.order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            offer_detail=self.offer_detail,
            title='Basic',
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            offer_type='basic',
            status='in_progress'
        )
        self.detail_url = reverse('order-detail', kwargs={'pk': self.order.pk})

    def test_patch_order_status_as_business_user(self):
        self.client.force_authenticate(user=self.business_user)
        response = self.client.patch(self.detail_url, {'status': 'completed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')

    def test_patch_order_status_as_customer(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.patch(self.detail_url, {'status': 'completed'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_order_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)

    def test_delete_order_as_customer(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OrderCountTest(APITestCase):

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
        self.offer = Offer.objects.create(
            user=self.business_user,
            title='Test Offer',
            description='Test'
        )
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title='Basic',
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            offer_type='basic'
        )
        Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            offer_detail=self.offer_detail,
            title='Basic',
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            offer_type='basic',
            status='in_progress'
        )
        Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            offer_detail=self.offer_detail,
            title='Basic',
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            offer_type='basic',
            status='completed'
        )
        self.count_url = reverse(
            'order-count', kwargs={'business_user_id': self.business_user.pk})
        self.completed_count_url = reverse(
            'completed-order-count', kwargs={'business_user_id': self.business_user.pk})

    def test_order_count(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(self.count_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_count'], 1)

    def test_completed_order_count(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(self.completed_count_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completed_order_count'], 1)
