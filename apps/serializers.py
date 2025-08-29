import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from apps.models import Category, Car, Review, CarImages, BillingInfo, RentalInfo, RentalOrder
from authentication.serializers import UserModelSerializer


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


class ReviewUpdateModelSerializer(ReviewModelSerializer):
    class Meta:
        model = Review
        fields = ('text', 'is_edited')
        read_only_fields = ('id', 'stars', 'user', 'car', 'created_at', 'updated_at', 'is_edited')

    def update(self, instance, validated_data):
        old_text = instance.text
        new_text = validated_data.get('text', old_text)

        if new_text != old_text:
            validated_data['is_edited'] = True

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserModelSerializer(instance.user).data if instance.user else None
        return data


class CarImagesModelSerializer(ModelSerializer):
    class Meta:
        model = CarImages
        fields = ('images', 'car')
        read_only_fields = ('id', 'created_at', 'updated_at')


class CarModelSerializer(ModelSerializer):
    reviews = ReviewModelSerializer(many=True, read_only=True)
    carimages_set = CarImagesModelSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = (
            'name', 'description', 'category', 'capacity', 'steering',
            'gasoline', 'price', 'main_image', 'reviews', 'carimages_set'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'telegram_message_id', 'carimages_set')

    def validate_price(self, value):
        if value < 0:
            raise ValidationError('The car price cannot be negative!')
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['reviews'] = ReviewModelSerializer(instance.reviews.all(), many=True).data
        data['carimages_set'] = CarImagesModelSerializer(
            instance.carimages_set.all(),
            many=True
        ).data
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


class BillingInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingInfo
        fields = ('full_name', 'phone', 'district')
        read_only_fields = ('id',)

    def validate_phone(self, value):
        phone = re.sub(r'\D', '', value)
        pattern = r'^998(90|91|93|94|95|97|98|99|33|88|50|77)\d{7}$'
        if not re.match(pattern, phone):
            raise serializers.ValidationError(
                'Telefon raqami quyidagi formatda bo‘lishi kerak: +998XXXXXXXXX'
            )
        return phone


class RentalInfoModelSerializer(serializers.ModelSerializer):
    car = CarModelSerializer(read_only=True)
    car_id = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all(), write_only=True, source="car"
    )

    class Meta:
        model = RentalInfo
        fields = ("pickup_location",
                  "pickup_date",
                  "pickup_time",
                  "dropoff_location",
                  "dropoff_date",
                  "dropoff_time",
                  "car",
                  "car_id",
                  )
        read_only_fields = ('id',)


# class PaymentModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentInfo
#         fields = ("method", "card_number", "expiry", "cvc", "holder")
#         read_only_fields = ('id', 'created_at',)
#
#     def validate_expiry(self, value):
#         digits = value.replace('-', '')
#         if len(digits) == 4 and digits.isdigit():
#             value = f"{digits[:2]}/{digits[2:]}"
#         import re
#         if not re.match(r'^(0[1-9]|1[0-2])/[0-9]{2}$', value):
#             raise ValidationError("Expiration date must be in the format MM/YY")
#         return value
#
#     def validate_holder(self, value):
#         import re
#         if not re.match(r'^[A-Z ]+$', value.upper()):
#             raise ValidationError("Card holder must be an uppercase letter")
#         return value.upper()
#
#     def save(self, **kwargs):
#         user = self.context['request'].user
#         user.save()
#         return user


class RentalOrderSerializer(serializers.ModelSerializer):
    billing = BillingInfoModelSerializer()
    rental = RentalInfoModelSerializer()

    # payment = PaymentModelSerializer()

    class Meta:
        model = RentalOrder
        fields = ("id", "billing", "rental", "created_at",)  # "payment"
        read_only_fields = ("id", "created_at")

    def create(self, validated_data):
        billing_data = validated_data.pop("billing")
        rental_data = validated_data.pop("rental")
        # payment_data = validated_data.pop("payment")

        user = self.context["request"].user

        billing = BillingInfo.objects.create(user=user, **billing_data)
        rental = RentalInfo.objects.create(**rental_data)
        # payment = PaymentInfo.objects.create(**payment_data)

        order = RentalOrder.objects.create(
            user=user,
            billing=billing,
            rental=rental,
            # payment=payment
        )
        return order


class RecentTransactionSerializer(ModelSerializer):
    car_name = CharField(source="car.name")
    car_category = CharField(source="car.category.name")

    class Meta:
        model = RentalInfo
        fields = (
            "car_name",
            "car_category",
            "pickup_date",
            "dropoff_date",
            "pickup_location",
            "dropoff_location",
        )
