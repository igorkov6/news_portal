# tasks.py
# ===============================================
# задачи celery
# ===============================================

from celery import shared_task
from .utils import mailing_new_post, mailing_week_report


# ===============================================
# задача рассылки сообщения
# ===============================================

# должна вызываться по событию
# mail_info.apply_async([post_id], countdown=2)
@shared_task
def mail_info(post_id):
    # рассылка сообщений подписчикам нового поста
    mailing_new_post(post_id=post_id)


# ===============================================
# задача рассылки отчета
# ===============================================

# должна вызываться планировщиком по расписанию
@shared_task
def mail_report():
    # еженедельная рассылка отчетов подписчикам
    mailing_week_report()
