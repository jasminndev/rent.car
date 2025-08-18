from aiogram.types import KeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_button(buttons: list[list[str]]) -> InlineKeyboardBuilder:
    ikb = InlineKeyboardBuilder()
    for row in buttons:
        ikb.row(*[KeyboardButton(text=_(text)) for text in row])
    return ikb


def get_add_view_keyboard():
    buttons = [
        [_("⏬ Rent") ],
        [_("⬅️ Back")]
    ]
    return build_button(buttons).as_markup()
