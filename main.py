import asyncio
import os

import django
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")
django.setup()

from apps.models import Car
from bot.core.config import conf

bot = Bot(token=conf.bot.BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    args = message.text.split()
    if len(args) > 1:
        id = args[1]
        try:
            car = Car.objects.get(id=id)
            await message.answer(f"Images: {car.main_image}Car ID: {car.id}\nPrice: {car.price}")
        except Car.DoesNotExist:
            await message.answer(f"Car not found!")
    else:
        await message.answer('Welcome! Send me a car id.')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
