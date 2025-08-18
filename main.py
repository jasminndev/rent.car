import asyncio
import os

import django
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, InputMediaPhoto, FSInputFile
from asgiref.sync import sync_to_async

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
        param = args[1]
        if param.startswith('car_'):
            try:
                car_id = int(param.split('_')[1])
            except (IndexError, ValueError):
                await message.answer("Invalid car ID!")
                return
        else:
            try:
                car_id = int(param)
            except ValueError:
                await message.answer("Invalid car ID!")
                return

        try:
            car = await sync_to_async(Car.objects.prefetch_related('carimages_set').get)(id=car_id)
            images = []
            if car.main_image:
                images.append(car.main_image)
            images.extend([ci.images for ci in car.carimages_set.all()])
            file_paths = [img.path for img in images if img]

            caption = (
                f"🚗 Name: {car.name}\n"
                f"💰 Price: {car.price}\n"
                f"⛽ Gasoline: {car.gasoline}\n"
                f"⚙ Steering: {car.steering}\n"
                f"👥 Capacity: {car.capacity}\n"
                # f"🗂 Category: {car.category}\n"
                f"📝 Description: {car.description}\n"
            )

            if file_paths:
                media = [InputMediaPhoto(media=FSInputFile(path)) for path in file_paths]
                media[0].caption = caption
                await message.answer_media_group(media=media)
            else:
                await message.answer(f"{caption}\nNo images available.")
        except Car.DoesNotExist:
            await message.answer(f"Car not found!")
    else:
        await message.answer('Welcome! Send me a car id.')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
