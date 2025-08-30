import asyncio
import os

import django
from aiogram import Bot

from bot.dispatcher import dp
from bot.sender import get_car_data, send_car_to_channel, update_car_post
from core.config import conf
from main import start

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")
django.setup()

bot = Bot(token=conf.bot.BOT_TOKEN)


async def run_django():
    process = await asyncio.create_subprocess_exec(
        "python", "manage.py", "runserver", "0.0.0.0:8000"
    )
    await process.wait()


async def run_bot():
    await start(dp)
    await get_car_data(dp)
    await send_car_to_channel(dp)
    await update_car_post(dp)
    await dp.start_polling(bot)


async def main():
    await asyncio.gather(
        run_django(),
        run_bot(),
    )


if __name__ == "__main__":
    asyncio.run(main())
