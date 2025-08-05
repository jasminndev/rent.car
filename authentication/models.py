from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.db.models import ImageField, Model, TextChoices, ForeignKey, CASCADE, TextField, DecimalField
from django.db.models.fields import CharField, DateField, IntegerField, TimeField, DateTimeField


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
    avatar = ImageField(upload_to='avatars/%Y/%m/%d/', null=True, blank=True)
    phone_number = CharField(max_length=20, unique=True)
    address = CharField(max_length=255)
    city = CharField(max_length=50)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []


class Payment(Model):
    class CardType(TextChoices):
        VISA = 'Visa', 'Visa'
        PAYPAL = 'PayPal', 'PayPal'
        BITCOIN = 'Bitcoin', 'Bitcoin'

    card_number = CharField(max_length=50)
    expiration_date = DateField()
    card_holder = CharField(max_length=50)
    cvv = CharField(max_length=4)
    card_type = CharField(max_length=10, choices=CardType.choices, default=CardType.VISA)
    user = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return f'{self.card_type} - {self.card_holder}'


class Category(Model):
    name = CharField(max_length=255)
    car_amount = IntegerField()


class Car(Model):
    class CapacityType(TextChoices):
        TWO = '2', '2'
        FOUR = '4', '4'
        SIX = '6', '6'
        EIGHT = '8', '8'

    class SteeringType(TextChoices):
        MANUAL = 'Manual', 'manual'
        POWER = 'Power', 'power'
        ELECTRIC = 'Electric', 'electric'
        HYBRAULIC = 'Hybraulic', 'hybraulic'

    name = CharField(max_length=50)
    description = TextField()
    category = ForeignKey(Category, on_delete=CASCADE)
    capacity = CharField(max_length=10, choices=CapacityType.choices, default=CapacityType.TWO)
    steering = CharField(max_length=15, choices=SteeringType.choices, default=SteeringType.MANUAL)
    gasoline = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    main_image = ImageField(upload_to='main_image/%Y/%m/%d/')


class CarImages(Model):
    images = ImageField(upload_to='car/%Y/%m/%d/')
    car = ForeignKey(Car, on_delete=CASCADE)


class Wishlist(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    car = ForeignKey(Car, on_delete=CASCADE)

    def __str__(self):
        return f'{self.user.first_name} - {self.user.last_name} wishlist'


class Review(Model):
    class StarsNumber(TextChoices):
        FIVE = '5', 'Five'
        FOUR = '4', 'Four'
        THREE = '3', 'Three'
        TWO = '2', 'Two'
        ONE = '1', 'One'

    stars = CharField(max_length=10, choices=StarsNumber.choices, default=StarsNumber.ONE)
    user = ForeignKey(User, on_delete=CASCADE)
    text = TextField()
    rating = IntegerField()
    car = ForeignKey(Car, on_delete=CASCADE)


class PickUp(Model):
    class LocationType(TextChoices):
        SHAYXONTOHUR = 'SHAYXONTOHUR', 'shayxontohur'
        UCHTEPA = 'UCHTEPA', 'uchtepa'
        YUNUSOBOD = 'YUNUSOBOD', 'yunusobod'
        YAKKASAROY = 'YAKKASAROY', 'yakkasaroy'
        OLMAZOR = 'OLMAZOR', 'olmazor'

    location = CharField(max_length=50, choices=LocationType.choices)
    date = DateField()
    time = TimeField()
    user = ForeignKey(User, on_delete=CASCADE)


class DropOff(Model):
    class LocationType(TextChoices):
        SHAYXONTOHUR = 'SHAYXONTOHUR', 'shayxontohur'
        UCHTEPA = 'UCHTEPA', 'uchtepa'
        YUNUSOBOD = 'YUNUSOBOD', 'yunusobod'
        YAKKASAROY = 'YAKKASAROY', 'yakkasaroy'
        OLMAZOR = 'OLMAZOR', 'olmazor'

    location = CharField(max_length=50, choices=LocationType.choices)
    date = DateField()
    time = TimeField()
    user = ForeignKey(User, on_delete=CASCADE)
