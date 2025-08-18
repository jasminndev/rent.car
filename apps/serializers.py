from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.models import Category, Car, Review, CarImages
from authentication.serializers import UserModelSerializer


# class PaymentModelSerializer(ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = ('expiration_date', 'card_holder', 'cvv', 'card_type',)
#         read_only_fields = ('id', 'created_at', 'user')
#
#     def validate_expiration_date(self, value):
#         digits = value.replace('-', '')
#         if len(digits) == 4 and digits.isdigit():
#             value = f"{digits[:2]}/{digits[2:]}"
#         import re
#         if not re.match(r'^(0[1-9]|1[0-2])/[0-9]{2}$', value):
#             raise ValidationError("Expiration date must be in the format MM/YY")
#         return value
#
#     def validate_card_holder(self, value):
#         import re
#         if not re.match(r'^[A-Z ]+$', value.upper()):
#             raise ValidationError("Card holder must be an uppercase letter")
#         return value.upper()
#
#     def save(self, **kwargs):
#         user = self.context['request'].user
#         user.save()
#         return user


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
        fields = ('stars', 'text', 'car')
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserModelSerializer(instance.user).data if instance.user else None
        return data


class CarImagesModelSerializer(ModelSerializer):
    class Meta:
        model = CarImages
        fields = ('images', 'car')
        read_only_fields = ('id', 'created_at', 'updated_at')


class BulkCarImagesSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        allow_empty=False
    )
    car = serializers.IntegerField(required=True)

    def create(self, validated_data):
        car_id = validated_data['car']
        images = validated_data['images']
        car_images = []
        for image in images:
            car_image = CarImages.objects.create(car_id=car_id, images=image)
            car_images.append(car_image)
        return car_images


class CarModelSerializer(ModelSerializer):
    reviews = ReviewModelSerializer(many=True, read_only=True)
    carimages_set = CarImagesModelSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = (
            'name', 'description', 'category', 'capacity', 'steering', 'gasoline', 'price', 'main_image', 'reviews',
            'carimages_set')
        read_only_fields = ('id', 'created_at', 'updated_at', 'telegram_message_id')

    def validate_price(self, value):
        if value < 0:
            raise ValidationError('The car price cannot be negative!')
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['reviews'] = ReviewModelSerializer(instance.reviews.all(), many=True).data
        data['carimages_set'] = CarImagesModelSerializer(instance.carimages_set.all().delete(),
                                                         many=True).data if instance.carimages_set else None
        return data

    def create(self, validated_data):
        carimages_data = validated_data.pop('carimages_set', [])
        car = Car.objects.create(**validated_data)
        for image_data in carimages_data:
            CarImages.objects.create(car=car, **image_data)
        return car

    def update(self, instance, validated_data):
        carimages_data = validated_data.pop('carimages_set', [])
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.capacity = validated_data.get('capacity', instance.capacity)
        instance.steering = validated_data.get('steering', instance.steering)
        instance.gasoline = validated_data.get('gasoline', instance.gasoline)
        instance.price = validated_data.get('price', instance.price)
        instance.main_image = validated_data.get('main_image', instance.main_image)
        instance.save()

        if carimages_data:
            instance.carimages_set.all().delete()
            for image_data in carimages_data:
                CarImages.objects.create(car=instance, **image_data)

        return instance


class ReviewUpdateModelSerializer(ReviewModelSerializer):
    class Meta:
        model = Review
        fields = ('text',)
        read_only_fields = ('id', 'stars', 'user', 'car', 'created_at', 'updated_at',)


class CarImagesModelSerializer(ModelSerializer):
    class Meta:
        model = CarImages
        fields = ('images',)
