from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message, SuccessfulPayment
from asgiref.sync import sync_to_async

from apps.models import Car, RentByBot, Location
from bot.dispatcher import dp
from bot.loader import bot
from bot.states import RentCarForm
from core.config import Payment

PAYMENT_PROVIDER_TOKEN = Payment.PAYMENT_PROVIDER_TOKEN


def build_summary(rent: RentByBot) -> str:
    car_name = getattr(rent.car, "name", rent.car_id)
    return (
        f"✅ Rental Saved!\n\n"
        f"👤 {rent.name}\n"
        f"📞 {rent.phone}\n"
        f"🚘 Car: {car_name}\n"
        f"📍 Pick up: {rent.pickup_location} on {rent.pickup_date} at {rent.pickup_time}\n"
        f"📍 Drop off: {rent.dropoff_location} on {rent.dropoff_date} at {rent.dropoff_time}\n\n"
        f"💳 Payment: {rent.payment_method}"
    )


@sync_to_async
def save_rent_to_db(data: dict, tg_user_id: int) -> RentByBot:
    car = Car.objects.get(id=data["car_id"])
    pickup_location = Location.objects.get(name=data["pickup_location"])
    dropoff_location = Location.objects.get(name=data["dropoff_location"])

    rent = RentByBot.objects.create(
        car=car,
        name=data["name"],
        phone=data["phone"],
        pickup_location=pickup_location,
        pickup_date=data["pickup_date"],
        pickup_time=data["pickup_time"],
        dropoff_location=dropoff_location,
        dropoff_date=data["dropoff_date"],
        dropoff_time=data["dropoff_time"],
        payment_method=data["payment_method"],
        tg_user_id=tg_user_id,
    )
    return RentByBot.objects.select_related("car", "pickup_location", "dropoff_location").get(id=rent.id)


@dp.callback_query(F.data.startswith("payment_"), StateFilter(RentCarForm.payment_method))
async def choose_payment(callback: CallbackQuery, state: FSMContext):
    method = callback.data.split("_", 1)[1]
    await state.update_data(payment_method=method)

    data = await state.get_data()
    rent = await save_rent_to_db(data, tg_user_id=callback.from_user.id)

    if method == "cash":
        await callback.message.answer(build_summary(rent) + "\n\n💵 Please pay in cash at pickup.")
        await state.clear()
        await callback.answer()
        return

    car_price_minor_units = int(rent.car.price * 100)

    prices = [LabeledPrice(label=f"Car Rental - {rent.car.name}", amount=car_price_minor_units)]

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Car Rental",
        description=f"Payment for renting {rent.car.name}",
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="UZS",
        prices=prices,
        start_parameter="car-rent",
        payload=f"rent:{rent.id}",
    )

    await callback.message.answer("💳 Invoice sent. Please complete your card payment.")
    await callback.answer()


@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@sync_to_async
def mark_paid(rent_id: int, charge_id: str, amount: int, currency: str):
    try:
        rent = (
            RentByBot.objects
            .select_related("car", "pickup_location", "dropoff_location")
            .get(id=rent_id)
        )
        rent.payment_status = "paid"
        rent.paid_amount = amount
        rent.paid_currency = currency
        rent.save(update_fields=[])
        return rent
    except RentByBot.DoesNotExist:
        return None


@dp.message(F.successful_payment)
async def successful_payment(message: Message, state: FSMContext):
    sp: SuccessfulPayment = message.successful_payment
    rent_id = None
    if sp.invoice_payload and ":" in sp.invoice_payload:
        _, rent_id_str = sp.invoice_payload.split(":", 1)
        if rent_id_str.isdigit():
            rent_id = int(rent_id_str)

    rent = None
    if rent_id:
        rent = await mark_paid(
            rent_id=rent_id,
            charge_id=sp.telegram_payment_charge_id,
            amount=sp.total_amount,
            currency=sp.currency,
        )

    if rent:
        await message.answer(
            "✅ Payment successful!\n\n"
            f"{build_summary(rent)}\n"
            f"💰 {sp.total_amount / 100} {sp.currency}\n"
        )
    else:
        await message.answer(
            "✅ Payment successful!\n"
            f"💰 {sp.total_amount / 100} {sp.currency}\n"
        )

    await state.clear()
