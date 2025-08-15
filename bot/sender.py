import asyncio

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InputMediaPhoto, FSInputFile
from asgiref.sync import sync_to_async

from apps.models import Car
from bot.core.config import conf


async def _send(car: Car):
    bot = Bot(
        token=conf.bot.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="Markdown")
    )
    link = f"https://t.me/{conf.bot.BOT_USERNAME}?start=car_{car.id}"
    caption = (
        f"🚗 **{car.name}**\n"
        f"📝 Description: {car.description}\n"
        f"🗂 Category: {car.category}\n"
        f"👥 Capacity: {car.capacity}\n"
        f"⚙ Steering: {car.steering}\n"
        f"⛽ Gasoline: {car.gasoline}\n"
        f"💰 Price: {car.price}\n\n"
        f"[View in bot]({link})"
    )
    if car.main_image:
        msg = await bot.send_photo(
            chat_id=conf.bot.CHANNEL_ID,
            photo=FSInputFile(car.main_image.path),
            caption=caption
        )
    else:
        msg = await bot.send_message(
            chat_id=conf.bot.CHANNEL_ID,
            text=caption
        )

    await sync_to_async(Car.objects.filter(pk=car.id).update)(
        telegram_message_id=msg.message_id
    )

    await bot.session.close()


def send_car_to_channel(car):
    asyncio.run(_send(car))


async def _update(car: Car):
    bot = Bot(
        token=conf.bot.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="Markdown")
    )
    link = f"https://t.me/{conf.bot.BOT_USERNAME}?start=car_{car.id}"
    caption = (
        f"🚗 **{car.name}**\n"
        f"📝 Description: {car.description}\n"
        f"🗂 Category: {car.category}\n"
        f"👥 Capacity: {car.capacity}\n"
        f"⚙ Steering: {car.steering}\n"
        f"⛽ Gasoline: {car.gasoline}\n"
        f"💰 Price: {car.price}\n\n"
        f"[View in bot]({link})"
    )
    if car.main_image:
        media = InputMediaPhoto(
            media=FSInputFile(car.main_image.path),
            caption=caption,
            parse_mode="Markdown"
        )
        await bot.edit_message_media(
            chat_id=conf.bot.CHANNEL_ID,
            message_id=car.telegram_message_id,
            media=media
        )
    else:
        await bot.edit_message_text(
            chat_id=conf.bot.CHANNEL_ID,
            message_id=car.telegram_message_id,
            text=caption
        )

    await bot.session.close()


def update_car_post(car):
    asyncio.run(_update(car))
