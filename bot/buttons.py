from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.config import BotConfig

locations_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Yunusobod", callback_data="loc_yunusobod")],
        [InlineKeyboardButton(text="Chilonzor", callback_data="loc_chilonzor")],
        [InlineKeyboardButton(text="Sergeli", callback_data="loc_sergeli")],
    ]
)

payment_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💵 Cash", callback_data="payment_cash")],
        [InlineKeyboardButton(text="💳 Card", callback_data="payment_card")],
    ]
)

BOT_USERNAME = BotConfig.BOT_USERNAME

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="See in channel",
                url=BOT_USERNAME
            )
        ]
    ]
)
