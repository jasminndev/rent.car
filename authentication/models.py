from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.db.models import ImageField, Model, DateTimeField, ForeignKey, CASCADE
from django.db.models.fields import CharField

from apps.models import Car


class CustomUserManager(UserManager):
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)

    create_superuser.alters_data = True

    async def acreate_superuser(
            self, phone_number, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return await self._acreate_user(phone_number, password, **extra_fields)

    def _create_user_object(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone_number must be set")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, phone_number, password, **extra_fields):
        user = self._create_user_object(phone_number, password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    first_name = CharField(max_length=35)
    last_name = CharField(max_length=35)
    avatar = ImageField(upload_to='avatars/%Y/%m/%d/', null=True, blank=True)
    phone_number = CharField(max_length=20, unique=True)
    address = CharField(max_length=255)
    city = CharField(max_length=50)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = CustomUserManager()
    username = None
    email = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []


class Wishlist(Model):
    user = ForeignKey('authentication.User', on_delete=CASCADE)
    car = ForeignKey('apps.Car', on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} - {self.user.last_name} wishlist'
