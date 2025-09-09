from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from core.config import BotConfig

BOT_TOKEN = BotConfig.BOT_TOKEN

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
