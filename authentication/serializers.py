import re

from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from orjson import orjson
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import Car
from authentication.models import User, Wishlist


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'avatar', 'password', 'district',)
        read_only_fields = ('date_joined', 'last_login')

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise ValidationError('Elektron pochta manzili yaroqsiz.')

        if User.objects.filter(email=value).exists():
            raise ValidationError('Bu elektron pochta manzili ro‘yxatdan o‘tgan.')

        return value

    def validate_password(self, value):
        if len(value) < 4:
            raise ValidationError('Password must be at least 4 characters long.')
        if len(value) > 20:
            raise ValidationError('Password must be at most 20 characters long.')
        if not re.search(r'\d', value):
            raise ValidationError('Password must contain at least one digit.')
        if not re.search(r'[A-Za-z]', value):
            raise ValidationError('Password must contain at least one letter.')

        return make_password(value)

    def validate_avatar(self, value):
        if value and not value.name.lower().endswith(('.jpg', 'jpeg', 'png')):
            raise ValidationError('Avatar must be an image.')
        return value


class VerifyCodeSerializer(Serializer):
    code = CharField(max_length=6)

    def validate_code(self, value):
        data = redis.get(value)
        if not data:
            raise ValidationError("Code notog'ri")
        user_data = orjson.loads(data)
        self.context['user_data'] = user_data
        return value


class UserUpdateSerializer(UserModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar',)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(Serializer):
    old_password = CharField(write_only=True, required=True)
    new_password = CharField(write_only=True, required=True)
    confirm_password = CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError('Old password is incorrect.')
        return value

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise ValidationError('New password and Confirm password must match.')
        if len(new_password) < 4:
            raise ValidationError('Password must be at least 4 characters long.')
        if len(new_password) > 20:
            raise ValidationError('Password must be at most 20 characters long.')
        if not re.search(r'\d', new_password):
            raise ValidationError('Password must contain at least one digit.')
        if not re.search(r'[A-Za-z]', new_password):
            raise ValidationError('Password must contain at least one letter.')

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class WishlistModelSerializer(ModelSerializer):
    from apps.serializers import CarModelSerializer
    car = CarModelSerializer(read_only=True)
    car_id = PrimaryKeyRelatedField(queryset=Car.objects.all(), write_only=True)

    class Meta:
        model = Wishlist
        fields = ('car', 'car_id')
        read_only_fields = ('id', 'car', 'user')

    def create(self, validated_data):
        car = validated_data.pop('car_id')
        validated_data['car'] = car
        return super().create(validated_data)
