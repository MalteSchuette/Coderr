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


class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, source='offer_details')

    def validate_details(self, value):
        if self.instance is None:  
            if len(value) != 3:
                raise serializers.ValidationError("Ein Offer muss genau 3 Details enthalten.")
            types = [detail['offer_type'] for detail in value]
            if sorted(types) != ['basic', 'premium', 'standard']:
                raise serializers.ValidationError("Ein Offer muss genau ein Basic, Standard und Premium Detail enthalten.")
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('offer_details')
        offer = Offer.objects.create(**validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop('offer_details', [])
        
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        
        for detail_data in details_data:
            offer_type = detail_data.get('offer_type')
            if offer_type:
                detail = instance.offer_details.get(offer_type=offer_type)
                for key, value in detail_data.items():
                    setattr(detail, key, value)
                detail.save()
        return instance

    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']