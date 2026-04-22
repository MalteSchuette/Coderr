from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Order
from .serializers import OrderSerializer
from .permissions import IsCustomerUser, IsBusinessOwner, IsAdminUser

User = get_user_model()

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsCustomerUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(customer_user=self.request.user)


class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), IsAdminUser()]
        if self.request.method == 'PATCH':
            return [permissions.IsAuthenticated(), IsBusinessOwner()]
        return [permissions.IsAuthenticated()]


class OrderCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_user_id):
        get_object_or_404(User, id=business_user_id)
        count = Order.objects.filter(
            business_user=business_user_id,
            status='in_progress'
        ).count()
        return Response({'order_count': count})


class CompletedOrderCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_user_id):
        get_object_or_404(User, id=business_user_id)
        count = Order.objects.filter(
            business_user=business_user_id,
            status='completed'
        ).count()
        return Response({'completed_order_count': count})
