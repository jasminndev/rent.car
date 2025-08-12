import asyncio

from aiogram import Bot

from bot.core.config import conf

bot = Bot(token=conf.TOKEN)


def run_async(func):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.ensure_future(func())
    else:
        loop.run_until_complete(func())


def send_car_to_channel(car):
    async def _send():
        msg = await bot.send_message(
            chat_id=conf.CHANNEL_ID,
            text=f"🚗 {car.name}\n💰 {car.price}\n\n"
                 f"[View in bot](https://t.me/{conf.BOT_USERNAME}?start={car.id})",
            parse_mode="Markdown"
        )
        car.telegram_message_id = msg.message_id
        car.save(update_fields=["telegram_message_id"])

    run_async(_send)


def update_car_post(car):
    async def _update():
        await bot.edit_message_text(
            chat_id=conf.CHANNEL_ID,
            message_id=car.telegram_message_id,
            text=f"🚗 {car.name}\n💰 {car.price}\n\n"
                 f"[View in bot](https://t.me/{conf.BOT_USERNAME}?start={car.id})",
            parse_mode="Markdown"
        )

    run_async(_update)
