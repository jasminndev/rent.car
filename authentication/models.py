from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.db.models import ImageField, Model, DateTimeField, ForeignKey, CASCADE
from django.db.models.fields import CharField, EmailField

from apps.models import Car


class CustomerUser(UserManager):
    def _create_user_object(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        user = self._create_user_object(email, password, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    first_name = CharField(max_length=35)
    last_name = CharField(max_length=35)
    avatar = ImageField(upload_to='avatars/%Y/%m/%d/', null=True, blank=True)
    email = EmailField(unique=True)
    district = ForeignKey('apps.District', on_delete=CASCADE, related_name='users', null=True, blank=True)
    updated_at = DateTimeField(auto_now=True)
    objects = CustomerUser()
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Wishlist(Model):
    user = ForeignKey('authentication.User', on_delete=CASCADE)
    car = ForeignKey('apps.Car', on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} - {self.user.last_name} wishlist'
