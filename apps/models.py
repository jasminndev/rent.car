from django.db.models import ImageField, Model, TextChoices, ForeignKey, CASCADE, TextField, DecimalField, DateTimeField
from django.db.models.fields import CharField, DateField, IntegerField, TimeField, BigIntegerField


class Payment(Model):
    class CardType(TextChoices):
        VISA = 'Visa', 'Visa'
        PAYPAL = 'PayPal', 'PayPal'
        BITCOIN = 'Bitcoin', 'Bitcoin'

    card_number = CharField(max_length=16)
    expiration_date = CharField(max_length=5)
    card_holder = CharField(max_length=50)
    cvv = CharField(max_length=3)
    card_type = CharField(max_length=10, choices=CardType.choices)
    user = ForeignKey('authentication.User', on_delete=CASCADE, related_name='payments')
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.card_type} - {self.card_holder}'


class Category(Model):
    name = CharField(max_length=255)
    car_amount = IntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class Car(Model):
    class CapacityType(TextChoices):
        TWO = '2', '2'
        FOUR = '4', '4'
        SIX = '6', '6'
        EIGHT_OR_MORE = '8 or more', '8 OR MORE'

    class SteeringType(TextChoices):
        MANUAL = 'Manual', 'manual'
        POWER = 'Power', 'power'
        ELECTRIC = 'Electric', 'electric'
        HYBRAULIC = 'Hybraulic', 'hybraulic'

    name = CharField(max_length=50)
    description = TextField()
    category = ForeignKey('apps.Category', on_delete=CASCADE, related_name='cars')
    capacity = CharField(max_length=10, choices=CapacityType.choices)
    steering = CharField(max_length=15, choices=SteeringType.choices)
    gasoline = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2, default=0)
    main_image = ImageField(upload_to='main_image/%Y/%m/%d/')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    telegram_message_id = BigIntegerField(null=True, blank=True)


class CarImages(Model):
    images = ImageField(upload_to='car/%Y/%m/%d/')
    car = ForeignKey('apps.Car', on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class Review(Model):
    class StarsNumber(TextChoices):
        FIVE = '5', 'Five'
        FOUR = '4', 'Four'
        THREE = '3', 'Three'
        TWO = '2', 'Two'
        ONE = '1', 'One'

    stars = CharField(max_length=10, choices=StarsNumber.choices)
    user = ForeignKey('authentication.User', on_delete=CASCADE, related_name='reviews')
    text = TextField()
    car = ForeignKey('apps.Car', on_delete=CASCADE, related_name='reviews')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


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
    user = ForeignKey('authentication.User', on_delete=CASCADE, related_name='pick_ups')


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
    user = ForeignKey('authentication.User', on_delete=CASCADE, related_name='drop_offs')
