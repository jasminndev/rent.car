from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

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


@dp.message(RentCarForm.name)
async def process_name(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.answer("Error: Name cannot be empty. Please enter your full name:")
        return
    await state.update_data(name=message.text.strip())
    await message.answer("📞 Enter your phone number:")
    await state.set_state(RentCarForm.phone)


@dp.message(RentCarForm.phone)
async def process_city(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.answer("Error: Phone number cannot be empty. Please enter your phone number:")
        return
    await state.update_data(city=message.text.strip())
    await message.answer("📍 Enter pickup location:")
    await state.set_state(RentCarForm.pickup_location)


@dp.message(RentCarForm.pickup_location)
async def process_pickup_location(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.answer("Error: Pickup location cannot be empty. Please enter pickup location:")
        return
    await state.update_data(pickup_location=message.text.strip())
    await message.answer("📅 Enter pickup date (YYYY-MM-DD):")
    await state.set_state(RentCarForm.pickup_date)


@dp.message(RentCarForm.pickup_date)
async def process_pickup_date(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.answer("Error: Pickup date cannot be empty. Please enter pickup date (YYYY-MM-DD):")
        return
    await state.update_data(pickup_date=message.text.strip())
    await message.answer("⏰ Enter pickup time (HH:MM):")
    await state.set_state(RentCarForm.pickup_time)


@dp.message(RentCarForm.pickup_time)
async def process_pickup_time(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.answer("Error: Pickup time cannot be empty. Please enter pickup time (HH:MM):")
        return
    await state.update_data(pickup_time=message.text.strip())
    await message.answer("📍 Enter dropoff location:")
    await state.set_state(RentCarForm.dropoff_location)


@dp.message(RentCarForm.dropoff_location)
async def process_dropoff_location(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.answer("Error: Dropoff location cannot be empty. Please enter dropoff location:")
        return
    await state.update_data(dropoff_location=message.text.strip())
    await message.answer("📅 Enter dropoff date (YYYY-MM-DD):")
    await state.set_state(RentCarForm.dropoff_date)


@dp.message(RentCarForm.dropoff_date)
async def process_dropoff_date(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.answer("Error: Dropoff date cannot be empty. Please enter dropoff date (YYYY-MM-DD):")
        return
    await state.update_data(dropoff_date=message.text.strip())
    await message.answer("⏰ Enter dropoff time (HH:MM):")
    await state.set_state(RentCarForm.dropoff_time)


@dp.message(RentCarForm.card_cvc)
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
        f"🏠 {data.get('address', 'N/A')}, {data.get('city', 'N/A')}\n\n"
        f"🚘 Car ID: {data.get('car_id', 'N/A')}\n"
        f"📍 Pickup: {data.get('pickup_location', 'N/A')} on {data.get('pickup_date', 'N/A')} at {data.get('pickup_time', 'N/A')}\n"
        f"📍 Dropoff: {data.get('dropoff_location', 'N/A')} on {data.get('dropoff_date', 'N/A')} at {data.get('dropoff_time', 'N/A')}\n\n"
        f"💳 Payment: {data.get('payment_method', 'N/A')} (Card ending {data.get('card_number', 'N/A')[-4:]})"
    )
    await message.answer(summary)
    await state.clear()
