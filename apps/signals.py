from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.models import Car
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
