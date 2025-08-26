from ckeditor.fields import RichTextField
from django.db.models import ImageField, Model, TextChoices, ForeignKey, CASCADE, DateTimeField, \
    OneToOneField, DateField, TimeField
from django.db.models.fields import CharField, BigIntegerField, PositiveIntegerField, BooleanField


class Region(Model):
    name = CharField(max_length=50)


class District(Model):
    name = CharField(max_length=50)
    region = ForeignKey(Region, on_delete=CASCADE, related_name='districts')


class Category(Model):
    name = CharField(max_length=50, db_index=True)
    car_amount = PositiveIntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


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

    name = CharField(max_length=50)
    description = RichTextField()
    category = ForeignKey('apps.Category', on_delete=CASCADE, related_name='cars')
    capacity = CharField(max_length=10, choices=CapacityType.choices)
    steering = CharField(max_length=15, choices=SteeringType.choices)
    gasoline = CharField(max_length=255)
    price = PositiveIntegerField(default=0)
    main_image = ImageField(upload_to='main_images/%Y/%m/%d/')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    telegram_message_id = BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class CarImages(Model):
    images = ImageField(upload_to='cars/%Y/%m/%d/')
    car = ForeignKey('apps.Car', on_delete=CASCADE, related_name='carimages_set')
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
    text = RichTextField()
    car = ForeignKey('apps.Car', on_delete=CASCADE, related_name='reviews')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_edited = BooleanField(default=False)


class BillingInfo(Model):
    user = ForeignKey('authentication.User', on_delete=CASCADE)
    full_name = CharField(max_length=100)
    phone = CharField(max_length=20)
    district = ForeignKey('apps.District', on_delete=CASCADE, related_name='billing_infos')

    def __str__(self):
        return f"{self.full_name} -> ({self.district.name})"


class LocationChoices(TextChoices):
    TASHKENT_AIRPORT = "TAS_AIR", "Tashkent Airport"
    TASHKENT_CITY = "TAS_CITY", "Tashkent City Center"
    SAMARKAND_STATION = "SAM_ST", "Samarkand Station"
    BUKHARA_DOWNTOWN = "BUH_DT", "Bukhara Downtown"


class RentalInfo(Model):
    car = ForeignKey("apps.Car", on_delete=CASCADE)
    pickup_location = CharField(max_length=20, choices=LocationChoices.choices)
    pickup_date = DateField()
    pickup_time = TimeField()
    dropoff_location = CharField(max_length=20, choices=LocationChoices.choices)
    dropoff_date = DateField()
    dropoff_time = TimeField()

    def __str__(self):
        return f"{self.car} | {self.pickup_location} → {self.dropoff_location}"


# class PaymentInfo(Model):
#     PAYMENT_METHODS = [
#         ("card", "Credit Card"),
#         ("paypal", "PayPal"),
#         ("btc", "Bitcoin"),
#     ]
#     method = CharField(max_length=20, choices=PAYMENT_METHODS)
#     card_number = CharField(max_length=16, blank=True, null=True)
#     expiry = CharField(max_length=5, blank=True, null=True)
#     holder = CharField(max_length=100, blank=True, null=True)
#     cvc = CharField(max_length=4, blank=True, null=True)
#     created_at = DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.method}"


class RentalOrder(Model):
    user = ForeignKey('authentication.User', on_delete=CASCADE)
    billing = OneToOneField(BillingInfo, on_delete=CASCADE)
    rental = OneToOneField(RentalInfo, on_delete=CASCADE)
    # payment = OneToOneField(PaymentInfo, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user}"
