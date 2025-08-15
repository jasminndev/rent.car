import asyncio

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from asgiref.sync import sync_to_async

from bot.core.config import conf


async def _send(car_id: int, name: str, price: str):
    bot = Bot(
        token=conf.bot.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="Markdown")
    )
    link = f"https://t.me/{conf.bot.BOT_USERNAME}?start=car_{car_id}"
    msg = await bot.send_message(
        chat_id=conf.bot.CHANNEL_ID,
        text=f"🚗 {name}\n💰 {price}\n\n[View in bot]({link})"
    )

    from apps.models import Car
    await sync_to_async(Car.objects.filter(pk=car_id).update)(
        telegram_message_id=msg.message_id
    )

    await bot.session.close()


def send_car_to_channel(car):
    asyncio.run(_send(car.id, car.name, str(car.price)))


async def _update(car_id: int, message_id: int, name: str, price: str):
    bot = Bot(
        token=conf.bot.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="Markdown")
    )
    link = f"https://t.me/{conf.bot.BOT_USERNAME}?start=car_{car_id}"
    await bot.edit_message_text(
        chat_id=conf.bot.CHANNEL_ID,
        message_id=message_id,
        text=f"🚗 {name}\n💰 {price}\n\n[View in bot]({link})"
    )

    await bot.session.close()


def update_car_post(car):
    asyncio.run(_update(car.id, car.telegram_message_id, car.name, str(car.price)))
