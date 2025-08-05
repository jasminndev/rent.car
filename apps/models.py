from django.db.models import ImageField, Model, TextChoices, ForeignKey, CASCADE, TextField, DecimalField
from django.db.models.fields import CharField, DateField, IntegerField, TimeField, DateTimeField


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
    user = ForeignKey('authentication.User', on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

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
    category = ForeignKey('apps.Category', on_delete=CASCADE)
    capacity = CharField(max_length=10, choices=CapacityType.choices, default=CapacityType.TWO)
    steering = CharField(max_length=15, choices=SteeringType.choices, default=SteeringType.MANUAL)
    gasoline = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    main_image = ImageField(upload_to='main_image/%Y/%m/%d/')


class CarImages(Model):
    images = ImageField(upload_to='car/%Y/%m/%d/')
    car = ForeignKey('apps.Car', on_delete=CASCADE)


class Review(Model):
    class StarsNumber(TextChoices):
        FIVE = '5', 'Five'
        FOUR = '4', 'Four'
        THREE = '3', 'Three'
        TWO = '2', 'Two'
        ONE = '1', 'One'

    stars = CharField(max_length=10, choices=StarsNumber.choices, default=StarsNumber.ONE)
    user = ForeignKey('authentication.User', on_delete=CASCADE)
    text = TextField()
    rating = IntegerField()
    car = ForeignKey('apps.Car', on_delete=CASCADE)


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
    user = ForeignKey('authentication.User', on_delete=CASCADE)


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
    user = ForeignKey('authentication.User', on_delete=CASCADE)
