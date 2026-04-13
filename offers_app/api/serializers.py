from rest_framework import serializers
from ..models import Offer, OfferDetail
from django.contrib.auth import get_user_model

User = get_user_model()


class OfferUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferDetailMinimalSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='offerdetail-detail')

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']


class OfferListSerializer(serializers.ModelSerializer):
    details = OfferDetailMinimalSerializer(many=True, read_only=True, source='offer_details')
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = OfferUserSerializer(source='user', read_only=True)

    def get_min_price(self, obj):
        return obj.offer_details.order_by('price').first().price

    def get_min_delivery_time(self, obj):
        return obj.offer_details.order_by('delivery_time_in_days').first().delivery_time_in_days

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']


class OfferRetrieveSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, read_only=True, source='offer_details')
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = OfferUserSerializer(source='user', read_only=True)

    def get_min_price(self, obj):
        return obj.offer_details.order_by('price').first().price

    def get_min_delivery_time(self, obj):
        return obj.offer_details.order_by('delivery_time_in_days').first().delivery_time_in_days

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']