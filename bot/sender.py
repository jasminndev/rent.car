from aiogram import Bot
from asgiref.sync import sync_to_async

from bot.core.config import conf

bot = Bot(token=conf.bot.BOT_TOKEN)

import asyncio


def run_async(coro):
    asyncio.run(coro)


def send_car_to_channel(car):
    async def _send():
        link = f"https://t.me/{conf.bot.BOT_USERNAME}?start=car_{car.id}"
        msg = await bot.send_message(
            chat_id=conf.bot.CHANNEL_ID,
            text=f"🚗 {car.name}\n💰 {car.price}\n\n"
                 f"[View in bot]({link})",
            parse_mode="Markdown"
        )
        car.telegram_message_id = msg.message_id
        await sync_to_async(car.save)(update_fields=["telegram_message_id"])

    run_async(_send())


def update_car_post(car):
    async def _update():
        await bot.edit_message_text(
            chat_id=conf.bot.CHANNEL_ID,
            message_id=car.telegram_message_id,
            text=f"🚗 {car.name}\n💰 {car.price}\n\n"
                 f"[View in bot](https://t.me/{conf.bot.BOT_USERNAME}?start={car.id})",
            parse_mode="Markdown"
        )

    run_async(_update())
