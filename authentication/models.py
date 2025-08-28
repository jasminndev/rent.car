from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import ImageField, Model, DateTimeField, ForeignKey, CASCADE
from django.db.models.fields import CharField, EmailField

from apps.models import Car


class CustomUserManager(UserManager):
    def _create_user_object(self, identifier, password, **extra_fields):
        if not identifier:
            raise ValueError("The given phone number or email must be set")

        if "@" in identifier:
            user = self.model(email=identifier, **extra_fields)
        else:
            user = self.model(phone_number=identifier, **extra_fields)

        user.password = make_password(password)
        return user

    def _create_user(self, identifier, password, **extra_fields):
        user = self._create_user_object(identifier, password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, identifier, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(identifier, password, **extra_fields)

    def create_superuser(self, identifier, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(identifier, password, **extra_fields)


class User(AbstractUser):
    first_name = CharField(max_length=35)
    last_name = CharField(max_length=35)
    avatar = ImageField(upload_to='avatars/%Y/%m/%d/', null=True, blank=True)
    phone_number = CharField(max_length=20, unique=True, null=True, blank=True)
    email = EmailField(unique=True, null=True, blank=True)
    updated_at = DateTimeField(auto_now=True)
    objects = CustomUserManager()
    username = None
    USERNAME_FIELD = 'phone_or_email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name + " " + self.last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def phone_or_email(self):
        return self.phone_number or self.email

    def clean(self):
        if not self.phone_number and not self.email:
            raise ValidationError('Phone or Email is required.')


class Wishlist(Model):
    user = ForeignKey('authentication.User', on_delete=CASCADE)
    car = ForeignKey('apps.Car', on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} - {self.user.last_name} wishlist'
