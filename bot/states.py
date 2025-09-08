from aiogram.fsm.state import StatesGroup, State


class RentCarForm(StatesGroup):
    name = State()
    phone = State()

    pickup_location = State()
    pickup_date = State()
    pickup_time = State()

    dropoff_location = State()
    dropoff_date = State()
    dropoff_time = State()

    payment_method = State()
    card_number = State()
    card_expiry = State()
    card_holder = State()
    card_cvc = State()
