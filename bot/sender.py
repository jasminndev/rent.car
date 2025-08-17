import asyncio

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InputMediaPhoto, FSInputFile
from asgiref.sync import sync_to_async

from apps.models import Car
from bot.core.config import conf


def get_car_data(car: Car):
    return {
        'id': car.id,
        'name': car.name,
        'description': car.description,
        'category': str(car.category),
        'capacity': car.capacity,
        'steering': car.steering,
        'gasoline': car.gasoline,
        'price': car.price,
        'main_image_path': car.main_image.path if car.main_image else None,
        'telegram_message_id': car.telegram_message_id,
    }


async def _send(car: Car):
    car_data = await sync_to_async(get_car_data)(car)

    bot = Bot(
        token=conf.bot.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="Markdown")
    )
    link = f"https://t.me/{conf.bot.BOT_USERNAME}?start=car_{car_data['id']}"
    caption = (
        f"🚗 **{car_data['name']}**\n"
        f"📝 Description: {car_data['description']}\n"
        f"🗂 Category: {car_data['category']}\n"
        f"👥 Capacity: {car_data['capacity']}\n"
        f"⚙ Steering: {car_data['steering']}\n"
        f"⛽ Gasoline: {car_data['gasoline']}\n"
        f"💰 Price: {car_data['price']}\n\n"
        f"[View in bot]({link})"
    )
    if car_data['main_image_path']:
        msg = await bot.send_photo(
            chat_id=conf.bot.CHANNEL_ID,
            photo=FSInputFile(car_data['main_image_path']),
            caption=caption
        )
    else:
        msg = await bot.send_message(
            chat_id=conf.bot.CHANNEL_ID,
            text=caption
        )

    await sync_to_async(Car.objects.filter(pk=car_data['id']).update)(
        telegram_message_id=msg.message_id
    )

    await bot.session.close()


def send_car_to_channel(car):
    asyncio.run(_send(car))


async def _update(car: Car):
    car_data = await sync_to_async(get_car_data)(car)

    bot = Bot(
        token=conf.bot.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="Markdown")
    )
    link = f"https://t.me/{conf.bot.BOT_USERNAME}?start=car_{car_data['id']}"
    caption = (
        f"🚗 **{car_data['name']}**\n"
        f"🗂 Category: {car_data['category']}\n"
        f"👥 Capacity: {car_data['capacity']}\n"
        f"⚙ Steering: {car_data['steering']}\n"
        f"⛽ Gasoline: {car_data['gasoline']}\n"
        f"💰 Price: {car_data['price']}\n\n"
        f"📝 Description: {car_data['description']}\n"
        f"[View in bot]({link})"
    )
    if car_data['main_image_path']:
        media = InputMediaPhoto(
            media=FSInputFile(car_data['main_image_path']),
            caption=caption,
            parse_mode="Markdown"
        )
        await bot.edit_message_media(
            chat_id=conf.bot.CHANNEL_ID,
            message_id=car_data['telegram_message_id'],
            media=media
        )
    else:
        await bot.edit_message_text(
            chat_id=conf.bot.CHANNEL_ID,
            message_id=car_data['telegram_message_id'],
            text=caption
        )

    await bot.session.close()


def update_car_post(car):
    asyncio.run(_update(car))
