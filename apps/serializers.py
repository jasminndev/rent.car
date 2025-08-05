from datetime import date
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.models import Payment , Category , Car , CarImages , Review , PickUp , DropOff


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ['expiration_date' , 'card_holder' , 'cvv' , 'card_type' , 'user']
        read_only_fields = ['id' , 'created_at']

    def validate_expiration_date(self, value):
        if value < date.today():
            return serializers.ValidationError('The card has expired !')
        return value


    def validate_cvv(self, value):
        if len(value) < 3 or len(value) > 3:
            return serializers.ValidationError('CVV must contain no less and no more than 3 digits !')
        return value


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name' , 'car_amount']


class CarSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = ['name' , 'description' , 'category' , 'capacity' , 'steering' , 'gasoline' , 'price' , 'main_image']


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['stars' , 'user' , 'text' , 'rating' , 'car']


class PickUpSerializer(ModelSerializer):
    class Meta:
        model = PickUp
        fields = ['location' , 'user']
        read_only_fields = ['id' , 'date' , 'time']


class DropOffSerializer(ModelSerializer):
    class Meta:
        model = DropOff
        fields = ['location' , 'user']
        read_only_fields = ['id' , 'date' , 'time']