from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.models import Car
from bot.sender import send_car_to_channel
from bot.sender import update_car_post


@receiver(post_save, sender=Car)
def send_or_update_car(sender, instance, created, **kwargs):
    if created:
        send_car_to_channel(instance)
    else:
        if instance.telegram_message_id:
            update_car_post(instance)
