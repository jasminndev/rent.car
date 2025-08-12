from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.models import Car


@receiver(post_save, sender=Car)
def send_or_update_car(sender, instance, created, **kwargs):
    if created:
        sender.send_car_to_channel(instance)
    else:
        if instance.telegram_message_id:
            sender.update_car_post(instance)
