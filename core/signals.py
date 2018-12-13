from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from core.models import *


@receiver(post_save, sender=NotificationModel)
def announce_new_notif(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
                "notif", {'type': 'notif',"event": "notificationupdate"})
        
@receiver(post_save, sender=ChatModel)
def announce_new_message(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
                "message", {'type': 'message',"event": "messageupdate"})
