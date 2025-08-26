from typing import Text

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot.dispatcher import dp
from bot.states import RentCarForm


@dp.callback_query(F.data.startswith("rent_"))
async def process_rent_button(callback: CallbackQuery, state: FSMContext):
    car_id = int(callback.data.split("_")[1])
    await state.update_data(car_id=car_id)

    await callback.message.answer("📝 Please enter your full name:")
    await state.set_state(RentCarForm.name)


@dp.message(RentCarForm.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📞 Enter your phone number:")
    await state.set_state(RentCarForm.phone)


@dp.message(RentCarForm.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("🏠 Enter your address:")
    await state.set_state(RentCarForm.address)


@dp.message(RentCarForm.address)
async def process_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("🌆 Enter your town / city:")
    await state.set_state(RentCarForm.city)


@dp.message(RentCarForm.dropoff_time)
async def ask_payment_method(message: Message, state: FSMContext):
    await state.update_data(dropoff_time=message.text)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Credit Card", callback_data="pay_card")],
            [InlineKeyboardButton(text="💲 PayPal", callback_data="pay_paypal")],
        ]
    )
    await message.answer("💰 Choose a payment method:", reply_markup=keyboard)
    await state.set_state(RentCarForm.payment_method)


@dp.message(RentCarForm.card_cvc)
async def confirm_order(message: Message, state: FSMContext):
    await state.update_data(card_cvc=message.text)
    data = await state.get_data()

    summary = (
        f"✅ Rental Summary\n\n"
        f"👤 {data['name']}\n"
        f"📞 {data['phone']}\n"
        f"🏠 {data['address']}, {data['city']}\n\n"
        f"🚘 Car ID: {data['car_id']}\n"
        f"📍 Pickup: {data['pickup_location']} on {data['pickup_date']} at {data['pickup_time']}\n"
        f"📍 Dropoff: {data['dropoff_location']} on {data['dropoff_date']} at {data['dropoff_time']}\n\n"
        f"💳 Payment: {data['payment_method']}"
    )

    await message.answer(summary)
    await state.clear()
