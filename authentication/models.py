from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.db.models import ImageField, Model, TextChoices, ForeignKey, CASCADE, TextField, DecimalField
from django.db.models.fields import CharField, DateField, IntegerField, TimeField


class CustomUserManager(UserManager):
    def _create_user_object(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone_number must be set")
        phone_number = self.normalize_phone_number(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, phone_number, password, **extra_fields):
        user = self._create_user_object(phone_number, password, **extra_fields)
        user.save(using=self._db)
        return user

    async def _acreate_user(self, phone_number, password, **extra_fields):
        user = self._create_user_object(phone_number, password, **extra_fields)
        await user.asave(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    create_user.alters_data = True

    async def acreate_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return await self._acreate_user(phone_number, password, **extra_fields)

    acreate_user.alters_data = True

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if not extra_fields["is_staff"]:
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields["is_superuser"]:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    first_name = CharField(max_length=35)
    last_name = CharField(max_length=35)
    avatar = ImageField(upload_to='avatars/', null=True, blank=True)
    phone_number = CharField(max_length=20)
    address = CharField(max_length=255)
    city = CharField(max_length=50)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['phone_number' , 'address', 'city']


class CardType(TextChoices):
    VISA = 'Visa', 'Visa'
    PAYPAL = 'PayPal', 'PayPal'
    BITCOIN = 'Bitcoin', 'Bitcoin'


class Payment(Model):
    card_number = CharField(max_length=50)
    expiration_date = DateField()
    card_holder = CharField(max_length=50)
    cvv = CharField(max_length=4)
    card_type = CharField(max_length=10, choices=CardType.choices)
    user = ForeignKey(User , on_delete=CASCADE)

    def __str__(self):
        return f'{self.card_type} - {self.card_holder}'

class Category(Model):
    name = CharField(max_length=255)
    car_amount = IntegerField()

class Capacity(TextChoices):
    TWO = '2' , '2'
    FOUR = '4' , '4'
    SIX = '6' , '6'
    EIGHT = '8' , '8'

class Steering(TextChoices):
    MANUAL = 'Manual' , 'manual'
    POWER = 'Power' , 'power'
    ELECTRIC = 'Electric' , 'electric'
    HYBRAULIC = 'Hybraulic' , 'hybraulic'

class Car(Model):
    name = CharField(max_length=50)
    description = TextField()
    category = ForeignKey(Category, on_delete=CASCADE)
    capacity = CharField(max_length=10 , choices=Capacity.choices)
    steering = CharField(max_length=15 , choices = Steering.choices)
    gasoline = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    main_image = ImageField(upload_to='images/')

class CarImages(Model):
    images = ImageField(upload_to='images/')
    car = ForeignKey(Car , on_delete=CASCADE)

class Wishlist(Model):
    user = ForeignKey(User , on_delete=CASCADE)
    car = ForeignKey(Car , on_delete=CASCADE)

    def __str__(self):
        return f'{self.user.first_name} - {self.user.last_name} wishlist'

class Review(Model):
    user = ForeignKey(User , on_delete=CASCADE)
    text = TextField()
    rating = IntegerField()
    car = ForeignKey(Car , on_delete=CASCADE)

class Location(TextChoices):
    SHAYXONTOHUR = 'SHAYXONTOHUR', 'shayxontohur'
    UCHTEPA = 'UCHTEPA', 'uchtepa'
    YUNUSOBOD = 'Yunusobod' , 'yunusobod'
    YAKKASAROY = 'Yakkasaroy' , 'yakkasaroy'
    OLMAZOR = 'OLMAZOR' , 'olmazor'

class PickUp(Model):
    location = CharField(max_length=50 , choices=Location.choices)
    date = DateField()
    time = TimeField()
    user = ForeignKey(User , on_delete=CASCADE)

class DropOff(Model):
    location = CharField(max_length=50 , choices=Location.choices)
    date = DateField()
    time = TimeField()
    user = ForeignKey(User , on_delete=CASCADE)

