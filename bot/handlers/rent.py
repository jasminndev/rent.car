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
        await callback.message.edit_text(f"📍 Pick up location selected: {location}")
        await callback.message.answer("📅 Select pick up date:", reply_markup=date_keyboard)
        await state.set_state(RentCarForm.pickup_date)

    elif current_state == RentCarForm.dropoff_location.state:
        await state.update_data(dropoff_location=location)
        await callback.message.edit_text(f"📍 Drop off location selected: {location}")
        await callback.message.answer("📅 Select drop off date:", reply_markup=date_keyboard)
        await state.set_state(RentCarForm.dropoff_date)

    await callback.answer()


@dp.callback_query(F.data.startswith("date_"), StateFilter(RentCarForm.pickup_date, RentCarForm.dropoff_date))
async def process_date(callback: CallbackQuery, state: FSMContext):
    date = callback.data.split("_")[1]
    current_state = await state.get_state()

    if current_state == RentCarForm.pickup_date.state:
        await state.update_data(pickup_date=date)
        await callback.message.edit_text(f"📅 Pick up date selected: {date}")
        await callback.message.answer("⏰ Select pick up time:", reply_markup=time_keyboard)
        await state.set_state(RentCarForm.pickup_time)

    elif current_state == RentCarForm.dropoff_date.state:
        await state.update_data(dropoff_date=date)
        await callback.message.edit_text(f"📅 Drop off date selected: {date}")
        await callback.message.answer("⏰ Select drop off time:", reply_markup=time_keyboard)
        await state.set_state(RentCarForm.dropoff_time)

    await callback.answer()


@dp.callback_query(F.data.startswith("time_"), StateFilter(RentCarForm.pickup_time, RentCarForm.dropoff_time))
async def process_time(callback: CallbackQuery, state: FSMContext):
    time = callback.data.split("_")[1]
    current_state = await state.get_state()

    if current_state == RentCarForm.pickup_time.state:
        await state.update_data(pickup_time=time)
        await callback.message.edit_text(f"⏰ Pick up time selected: {time}")
        await callback.message.answer("📍 Select drop off location:", reply_markup=locations_keyboard)
        await state.set_state(RentCarForm.dropoff_location)

    elif current_state == RentCarForm.dropoff_time.state:
        await state.update_data(dropoff_time=time)
        await callback.message.edit_text(f"⏰ Drop off time selected: {time}")
        await callback.message.answer("💰 Payment", reply_markup=payment_keyboard)
        await state.set_state(RentCarForm.payment_method)

    await callback.answer()
