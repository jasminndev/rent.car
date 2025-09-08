from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.buttons import locations_keyboard, date_keyboard, time_keyboard, payment_keyboard
from bot.dispatcher import dp
from bot.states import RentCarForm


@dp.callback_query(F.data.startswith("rent_"))
async def process_rent_button(callback: CallbackQuery, state: FSMContext):
    try:
        car_id = int(callback.data.split("_")[1])
        await state.update_data(car_id=car_id)
        await state.set_state(RentCarForm.name)
        await callback.message.edit_text("📝 Please enter your full name:")
    except (IndexError, ValueError):
        await callback.message.answer("Error: Invalid car ID!")
    await callback.answer()


@dp.message(StateFilter(RentCarForm.name))
async def process_name(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.answer("Error: Name cannot be empty. Please enter your full name:")
        return
    await state.update_data(name=message.text.strip())
    await message.answer("📞 Enter your phone number:")
    await state.set_state(RentCarForm.phone)


@dp.message(StateFilter(RentCarForm.phone))
async def process_phone(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.answer("Error: Phone number cannot be empty. Please enter your phone number:")
        return
    await state.update_data(phone=message.text.strip())
    await message.answer("📍 Select pickup location:", reply_markup=locations_keyboard)
    await state.set_state(RentCarForm.pickup_location)


@dp.callback_query(F.data.startswith("loc_"), StateFilter(RentCarForm.pickup_location, RentCarForm.dropoff_location))
async def process_location(callback: CallbackQuery, state: FSMContext):
    location = callback.data.split("_")[1].capitalize()
    current_state = await state.get_state()

    if current_state == RentCarForm.pickup_location.state:
        await state.update_data(pickup_location=location)
        await callback.message.edit_text(f"📍 Pickup location selected: {location}")
        await callback.message.answer("📅 Select pickup date:", reply_markup=date_keyboard)
        await state.set_state(RentCarForm.pickup_date)

    elif current_state == RentCarForm.dropoff_location.state:
        await state.update_data(dropoff_location=location)
        await callback.message.edit_text(f"📍 Dropoff location selected: {location}")
        await callback.message.answer("📅 Select dropoff date:", reply_markup=date_keyboard)
        await state.set_state(RentCarForm.dropoff_date)

    await callback.answer()


@dp.callback_query(F.data.startswith("date_"), StateFilter(RentCarForm.pickup_date, RentCarForm.dropoff_date))
async def process_date(callback: CallbackQuery, state: FSMContext):
    date = callback.data.split("_")[1]
    current_state = await state.get_state()

    if current_state == RentCarForm.pickup_date.state:
        await state.update_data(pickup_date=date)
        await callback.message.edit_text(f"📅 Pickup date selected: {date}")
        await callback.message.answer("⏰ Select pickup time:", reply_markup=time_keyboard)
        await state.set_state(RentCarForm.pickup_time)

    elif current_state == RentCarForm.dropoff_date.state:
        await state.update_data(dropoff_date=date)
        await callback.message.edit_text(f"📅 Dropoff date selected: {date}")
        await callback.message.answer("⏰ Select dropoff time:", reply_markup=time_keyboard)
        await state.set_state(RentCarForm.dropoff_time)

    await callback.answer()


@dp.callback_query(F.data.startswith("time_"), StateFilter(RentCarForm.pickup_time, RentCarForm.dropoff_time))
async def process_time(callback: CallbackQuery, state: FSMContext):
    time = callback.data.split("_")[1]
    current_state = await state.get_state()

    if current_state == RentCarForm.pickup_time.state:
        await state.update_data(pickup_time=time)
        await callback.message.edit_text(f"⏰ Pickup time selected: {time}")
        await callback.message.answer("📍 Select dropoff location:", reply_markup=locations_keyboard)
        await state.set_state(RentCarForm.dropoff_location)

    elif current_state == RentCarForm.dropoff_time.state:
        await state.update_data(dropoff_time=time)
        await callback.message.edit_text(f"⏰ Dropoff time selected: {time}")
        await callback.message.answer("💰 Choose a payment method:", reply_markup=payment_keyboard)
        await state.set_state(RentCarForm.payment_method)

    await callback.answer()


@dp.callback_query(F.data == "pay_card", StateFilter(RentCarForm.payment_method))
async def process_pay_card(callback: CallbackQuery, state: FSMContext):
    await state.update_data(payment_method="Credit Card")
    await callback.message.edit_text("💳 Enter card number:")
    await state.set_state(RentCarForm.card_number)
    await callback.answer()


@dp.message(StateFilter(RentCarForm.card_number))
async def process_card_number(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.answer("Error: Card number cannot be empty. Please enter card number:")
        return
    await state.update_data(card_number=message.text.strip())
    await message.answer("📅 Enter card expiry (MM/YY):")
    await state.set_state(RentCarForm.card_expiry)


@dp.message(StateFilter(RentCarForm.card_expiry))
async def process_card_expiry(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.answer("Error: Card expiry cannot be empty. Please enter card expiry (MM/YY):")
        return
    await state.update_data(card_expiry=message.text.strip())
    await message.answer("🔒 Enter card CVC:")
    await state.set_state(RentCarForm.card_cvc)


@dp.message(StateFilter(RentCarForm.card_cvc))
async def process_card_cvc(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.answer("Error: Card CVC cannot be empty. Please enter card CVC:")
        return

    await state.update_data(card_cvc=message.text.strip())
    data = await state.get_data()

    summary = (
        f"✅ Rental Summary\n\n"
        f"👤 {data.get('name', 'N/A')}\n"
        f"📞 {data.get('phone', 'N/A')}\n"
        f"🚘 Car ID: {data.get('car_id', 'N/A')}\n"
        f"📍 Pickup: {data.get('pickup_location', 'N/A')} on {data.get('pickup_date', 'N/A')} at {data.get('pickup_time', 'N/A')}\n"
        f"📍 Dropoff: {data.get('dropoff_location', 'N/A')} on {data.get('dropoff_date', 'N/A')} at {data.get('dropoff_time', 'N/A')}\n\n"
        f"💳 Payment: {data.get('payment_method', 'N/A')} (Card ending {data.get('card_number', 'N/A')[-4:]})"
    )

    await message.answer(summary)
    await state.clear()
