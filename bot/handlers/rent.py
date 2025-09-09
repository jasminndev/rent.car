import re
from datetime import datetime

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.buttons import locations_keyboard, payment_keyboard
from bot.dispatcher import dp
from bot.states import RentCarForm

DATE_PATTERN = re.compile(r"^\d{2}:\d{2}:\d{4}$")
TIME_PATTERN = re.compile(r"^\d{2}:\d{2}$")
PHONE_PATTERN = re.compile(r"^\+?\d{7,15}$")


def validate_date(date_str: str) -> bool:
    if not DATE_PATTERN.match(date_str):
        return False
    try:
        datetime.strptime(date_str, "%d:%m:%Y")
        return True
    except ValueError:
        return False


def validate_time(time_str: str) -> bool:
    if not TIME_PATTERN.match(time_str):
        return False
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


@dp.callback_query(F.data.startswith("rent_"))
async def process_rent_button(callback: CallbackQuery, state: FSMContext):
    try:
        car_id = int(callback.data.split("_")[1])
        await state.update_data(car_id=car_id)
        await state.set_state(RentCarForm.name)
        await callback.message.edit_text("📝 Please enter your full name:")
    except (IndexError, ValueError):
        await callback.message.answer("❌ Error: Invalid car ID!")
    await callback.answer()


@dp.message(StateFilter(RentCarForm.name))
async def process_name(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.answer("❌ Name cannot be empty. Please enter your full name:")
        return
    await state.update_data(name=message.text.strip())
    await message.answer("📞 Enter your phone number (e.g. +998901234567):")
    await state.set_state(RentCarForm.phone)


@dp.message(StateFilter(RentCarForm.phone))
async def process_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    if not PHONE_PATTERN.match(phone):
        await message.answer("❌ Invalid phone number format. Please enter again (e.g. +998901234567):")
        return

    await state.update_data(phone=phone)
    await message.answer("📍 Select pickup location:", reply_markup=locations_keyboard)
    await state.set_state(RentCarForm.pickup_location)


@dp.callback_query(F.data.startswith("loc_"), StateFilter(RentCarForm.pickup_location, RentCarForm.dropoff_location))
async def process_location(callback: CallbackQuery, state: FSMContext):
    location = callback.data.split("_")[1].capitalize()
    current_state = await state.get_state()

    if current_state == RentCarForm.pickup_location.state:
        await state.update_data(pickup_location=location)
        await callback.message.edit_text(f"📍 Pick up location selected: {location}")
        await callback.message.answer("📅 Enter pick up date (DD:MM:YYYY):")
        await state.set_state(RentCarForm.pickup_date)

    elif current_state == RentCarForm.dropoff_location.state:
        await state.update_data(dropoff_location=location)
        await callback.message.edit_text(f"📍 Drop off location selected: {location}")
        await callback.message.answer("📅 Enter drop off date (DD:MM:YYYY):")
        await state.set_state(RentCarForm.dropoff_date)

    await callback.answer()


@dp.message(StateFilter(RentCarForm.pickup_date))
async def process_pickup_date(message: Message, state: FSMContext):
    if not validate_date(message.text.strip()):
        await message.answer("❌ Invalid format! Enter pick up date in format DD:MM:YYYY")
        return
    await state.update_data(pickup_date=message.text.strip())
    await message.answer("⏰ Enter pick up time (HH:MM):")
    await state.set_state(RentCarForm.pickup_time)


@dp.message(StateFilter(RentCarForm.pickup_time))
async def process_pickup_time(message: Message, state: FSMContext):
    if not validate_time(message.text.strip()):
        await message.answer("❌ Invalid format! Enter pick up time in format HH:MM")
        return
    await state.update_data(pickup_time=message.text.strip())
    await message.answer("📍 Select drop off location:", reply_markup=locations_keyboard)
    await state.set_state(RentCarForm.dropoff_location)


@dp.message(StateFilter(RentCarForm.dropoff_date))
async def process_dropoff_date(message: Message, state: FSMContext):
    if not validate_date(message.text.strip()):
        await message.answer("❌ Invalid format! Enter drop off date in format DD:MM:YYYY")
        return
    await state.update_data(dropoff_date=message.text.strip())
    await message.answer("⏰ Enter drop off time (HH:MM):")
    await state.set_state(RentCarForm.dropoff_time)


@dp.message(StateFilter(RentCarForm.dropoff_time))
async def process_dropoff_time(message: Message, state: FSMContext):
    if not validate_time(message.text.strip()):
        await message.answer("❌ Invalid format! Enter drop off time in format HH:MM")
        return
    await state.update_data(dropoff_time=message.text.strip())
    await message.answer("💰 Select payment method:", reply_markup=payment_keyboard)
    await state.set_state(RentCarForm.payment_method)
