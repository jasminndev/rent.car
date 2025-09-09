import asyncio

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.models import Car, RentByBot
from bot.buttons import keyboard
from bot.loader import bot
from bot.sender import send_car_to_channel, update_car_post


@receiver(post_save, sender=Car)
def send_or_update_car(sender, instance: Car, created: bool, update_fields=None, **kwargs):
    if update_fields is not None:
        uf = set(update_fields) if not isinstance(update_fields, set) else update_fields
        if uf == {"telegram_message_id"}:
            return

    if created:
        send_car_to_channel(instance)
    elif instance.telegram_message_id:
        update_car_post(instance)


@receiver(post_save, sender=Car)
def notify_users_about_car(sender, instance: Car, created, **kwargs):
    if created:
        car = instance

        user_ids = list(
            RentByBot.objects.filter(car__name__icontains=car.name)
            .values_list("tg_user_id", flat=True)
            .distinct()
        )

        if user_ids:
            text = (
                f"🚘 A similar car that you ordered before is available again!\n\n"
                f"📌 {car.name}\n"
                f"💰 Price: {car.price}\n"
                f"⚙️ Details: {car.description or 'No details'}"
            )

            for user_id in user_ids:
                try:
                    asyncio.run(bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard))
                except Exception as e:
                    print(f"Error sending notification: {e}")
