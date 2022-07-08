# news/signals.py
# ===============================================
# сигналы
# ===============================================

from .models import Post
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .tasks import mail_info
from loguru import logger


# ===============================================
# обработка сигнала сохранения поста
# вызывается с задержкой для гарантированного завершения всех транзакций
# ===============================================
@receiver(signal=post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    # TODO uncomment for work
    # transaction.on_commit(lambda: mail_info.apply_async([instance.id], countdown=2))
    logger.debug(f'save post id= {instance.id}')
