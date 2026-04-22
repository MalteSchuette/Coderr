from rest_framework import serializers
from ..models import Offer, OfferDetail
from django.contrib.auth import get_user_model

User = get_user_model()


class OfferUserSerializer(serializers.ModelSerializer):
    """Minimal user representation embedded in offer responses."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class OfferDetailSerializer(serializers.ModelSerializer):
    """Full serializer for a single OfferDetail, used in create/update and detail views."""

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type']
        read_only_fields = ['id']


class OfferDetailMinimalSerializer(serializers.ModelSerializer):
    """Lightweight OfferDetail representation exposing only id and hypermedia URL."""

    url = serializers.HyperlinkedIdentityField(view_name='offerdetail-detail')

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']


class OfferListSerializer(serializers.ModelSerializer):
    """Read-only serializer for the offer list view with computed aggregate fields."""

    details = OfferDetailMinimalSerializer(
        many=True, read_only=True, source='offer_details')
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = OfferUserSerializer(source='user', read_only=True)

    def get_min_price(self, obj):
        """Return the lowest price across all offer details, or None if no details exist."""
        details = obj.offer_details.all()
        if not details:
            return None
        return min(detail.price for detail in details)

    def get_min_delivery_time(self, obj):
        """Return the shortest delivery time across all offer details, or None if no details exist."""
        details = obj.offer_details.all()
        if not details:
            return None
        return min(detail.delivery_time_in_days for detail in details)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at',
                  'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']


class OfferRetrieveSerializer(serializers.ModelSerializer):
    """Read-only serializer for a single offer detail view with full OfferDetail objects."""

    details = OfferDetailSerializer(
        many=True, read_only=True, source='offer_details')
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = OfferUserSerializer(source='user', read_only=True)

    def get_min_price(self, obj):
        """Return the lowest price across all offer details, or None if no details exist."""
        details = obj.offer_details.all()
        if not details:
            return None
        return min(detail.price for detail in details)

    def get_min_delivery_time(self, obj):
        """Return the shortest delivery time across all offer details, or None if no details exist."""
        details = obj.offer_details.all()
        if not details:
            return None
        return min(detail.delivery_time_in_days for detail in details)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at',
                  'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']


class OfferCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating offers including nested OfferDetail objects."""

    details = OfferDetailSerializer(many=True, source='offer_details')

    def validate_details(self, value):
        """Ensure exactly one basic, standard, and premium detail is provided on creation."""
        if self.instance is None:
            if len(value) != 3:
                raise serializers.ValidationError(
                    "Ein Offer muss genau 3 Details enthalten.")
            types = [detail['offer_type'] for detail in value]
            # Sorted comparison guarantees order-independent equality check
            if sorted(types) != ['basic', 'premium', 'standard']:
                raise serializers.ValidationError(
                    "Ein Offer muss genau ein Basic, Standard und Premium Detail enthalten.")
        return value

    def create(self, validated_data):
        """Create an Offer and its associated OfferDetail records in a single operation."""
        details_data = validated_data.pop('offer_details')
        offer = Offer.objects.create(**validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer

    def update(self, instance, validated_data):
        """Update an Offer and patch existing OfferDetail records matched by offer_type."""
        details_data = validated_data.pop('offer_details', [])

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        for detail_data in details_data:
            offer_type = detail_data.get('offer_type')
            if not offer_type:
                raise serializers.ValidationError(
                    {'offer_type': 'offer_type ist erforderlich um ein Detail zu aktualisieren.'})
            try:
                # Look up the existing detail by type; new types cannot be created via update
                detail = instance.offer_details.get(offer_type=offer_type)
            except OfferDetail.DoesNotExist:
                raise serializers.ValidationError(
                    {'offer_type': f'Kein Detail mit offer_type "{offer_type}" gefunden.'})
            for key, value in detail_data.items():
                setattr(detail, key, value)
            detail.save()
        return instance

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
        read_only_fields = ['id']
