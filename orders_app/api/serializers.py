from rest_framework import serializers

from offers_app.models import OfferDetail
from ..models import Order


class OrderSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        offer_detail_id = validated_data.pop('offer_detail_id')
        try:
            offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError(
                {'offer_detail_id': 'OfferDetail does not exist.'})

        order = Order.objects.create(
            offer_detail=offer_detail,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            **validated_data
        )
        return order

    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'business_user', 'offer_detail_id',
            'title', 'revisions', 'delivery_time_in_days', 'price',
            'features', 'offer_type', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'title', 'revisions', 'delivery_time_in_days', 'price',
            'features', 'offer_type', 'customer_user', 'business_user'
        ]
