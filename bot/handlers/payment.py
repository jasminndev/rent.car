from aiogram import F
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message
from asgiref.sync import sync_to_async

from apps.models import Car
from bot.dispatcher import dp
from core.config import Payment
from main import bot

PAYMENT_PROVIDER_TOKEN = Payment.PAYMENT_PROVIDER_TOKEN


@dp.callback_query(F.data == "invoice")
async def pay_card(callback: CallbackQuery):
    car = await sync_to_async(lambda: Car.objects.first())()

    prices = [
        LabeledPrice(label=f"Car Rental - {car.name}", amount=int(car.price * 100))
    ]

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Car Rental",
        description=f"Payment for renting {car.name}",
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="UZS",
        prices=prices,
        start_parameter="car-rent",
        payload=f"rent_car_{car.id}"
    )
    await callback.answer()


@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message(lambda m: m.content_type == "successful_payment")
async def successful_payment(message: Message):
    payment_info = message.successful_payment.to_python()
    await message.answer(
        f"✅ Payment successful!\n"
        f"💰 {payment_info['total_amount'] / 100} {payment_info['currency']}\n"
        f"📦 Payload: {payment_info['invoice_payload']}"
    )
