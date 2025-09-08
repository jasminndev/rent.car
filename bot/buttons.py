from aiogram.types import KeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_button(buttons: list[list[str]]) -> InlineKeyboardBuilder:
    ikb = InlineKeyboardBuilder()
    for row in buttons:
        ikb.row(*[KeyboardButton(text=_(text)) for text in row])
    return ikb


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

locations_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🛫 Airport", callback_data="loc_airport")],
        [InlineKeyboardButton(text="🏙 Downtown", callback_data="loc_downtown")],
        [InlineKeyboardButton(text="🏘 Suburb", callback_data="loc_suburb")],
    ]
)

date_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="2025-09-08", callback_data="date_2025-09-08"),
         InlineKeyboardButton(text="2025-09-09", callback_data="date_2025-09-09"),
         InlineKeyboardButton(text="2025-09-10", callback_data="date_2025-09-10")],
        [InlineKeyboardButton(text="2025-09-11", callback_data="date_2025-09-11"),
         InlineKeyboardButton(text="2025-09-12", callback_data="date_2025-09-12"),
         InlineKeyboardButton(text="2025-09-13", callback_data="date_2025-09-13")],
    ]
)

time_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="09:00", callback_data="time_09:00"),
         InlineKeyboardButton(text="09:15", callback_data="time_09:15"),
         InlineKeyboardButton(text="09:30", callback_data="time_09:30"),
         InlineKeyboardButton(text="09:45", callback_data="time_09:45")],
        [InlineKeyboardButton(text="10:00", callback_data="time_10:00"),
         InlineKeyboardButton(text="10:15", callback_data="time_10:15"),
         InlineKeyboardButton(text="10:30", callback_data="time_10:30"),
         InlineKeyboardButton(text="10:45", callback_data="time_10:45")],
    ]
)

payment_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💳 Invoice", callback_data="invoice")],
    ]
)
