from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.models import Payment, Category, Car, Review, PickUp, DropOff
from authentication.serializers import UserModelSerializer


class PaymentModelSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ('expiration_date', 'card_holder', 'cvv', 'card_type', 'user',)
        read_only_fields = ('id', 'created_at')

    def validate_expiration_date(self, value):
        digits = value.replace('-', '')
        if len(digits) == 4 and digits.isdigit():
            value = f"{digits[:2]}/{digits[2:]}"
        import re
        if not re.match(r'^(0[1-9]|1[0-2])/[0-9]{2}$', value):
            raise ValidationError("Expiration date must be in the format MM/YY")
        return value

    def validate_card_holder(self, value):
        import re
        if not re.match(r'^[A-Z ]+$', value.upper()):
            raise ValidationError("Card holder must be an uppercase letter")
        return value.upper()


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'car_amount')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_card_amount(self, value):
        if value < 0:
            return ValidationError('The card amount cannot be negative!')


class ReviewModelSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ('stars', 'text')
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserModelSerializer(instance.user).data if instance.user else None
        return data


class CarModelSerializer(ModelSerializer):
    reviews = ReviewModelSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = (
            'name', 'description', 'category', 'capacity', 'steering', 'gasoline', 'price', 'main_image', 'reviews')
        read_only_fields = ('id', 'created_at', 'updated_at',)

    def validate_price(self, value):
        if value < 0:
            return ValidationError('The car price cannot be negative!')
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['reviews'] = ReviewModelSerializer(instance.reviews.all(), many=True).data if instance.reviews else None
        return data


class ReviewUpdateModelSerializer(ReviewModelSerializer):
    class Meta:
        model = Review
        fields = ('text',)
        read_only_fields = ('id', 'stars', 'user', 'car', 'created_at', 'updated_at',)


class PickUpModelSerializer(ModelSerializer):
    class Meta:
        model = PickUp
        fields = ('location', 'user', 'date', 'time')
        read_only_fields = ('id',)


class DropOffModelSerializer(ModelSerializer):
    class Meta:
        model = DropOff
        fields = ('location', 'user', 'date', 'time')
        read_only_fields = ('id',)
