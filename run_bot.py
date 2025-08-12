import asyncio
import os

import django
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from apps.models import Car
from bot.core.config import conf

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")
django.setup()

bot = Bot(token=conf.TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    args = message.text.split()
    if len(args) > 1:
        car_id = args[1]
        try:
            car = Car.objects.get(id=car_id)
            await message.answer(f"Car ID: {car.id}\nPrice: {car.price}")
        except Car.DoesNotExist:
            await message.answer(f"Car not found!")
    else:
        await message.answer('Welcome! Send me a car id.')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
