from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message, SuccessfulPayment
from asgiref.sync import sync_to_async

from apps.models import Car
from bot.dispatcher import dp
from bot.states import RentCarForm
from core.config import Payment
from main import bot

PAYMENT_PROVIDER_TOKEN = Payment.PAYMENT_PROVIDER_TOKEN


@dp.callback_query(F.data.startswith("payment_"), StateFilter(RentCarForm.payment_method))
async def process_payment_callback(callback: CallbackQuery, state: FSMContext):
    payment = callback.data.replace("payment_", "")
    await state.update_data(payment_method=payment)

    if payment == "cash":
        await callback.message.answer(
            "💵 You selected cash.\n\n"
            "Please pay at the pick up location."
        )
        await state.set_state(RentCarForm.confirm)
        await callback.answer()
    else:
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


@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    sp: SuccessfulPayment = message.successful_payment
    await message.answer(
        f"✅ Payment successful!\n"
        f"💰 {sp.total_amount / 100} {sp.currency}\n"
        f"📦 Payload: {sp.invoice_payload}"
    )
