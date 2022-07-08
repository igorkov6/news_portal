# utils.py
# ===============================================
# общие функции
# ===============================================

import os
from .settings import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, PostCategory, Subscriber, SubscriberCategory
import datetime
from loguru import logger


# ===============================================
# получить список тем поста
# ===============================================
def get_category_list(post_id):

    # получить список PostCategory, для которых pos.id = post_id
    pc_list = PostCategory.objects.filter(post=Post.objects.get(id=post_id))

    # возвратить строку названий категорий
    return ', '.join(list(map(lambda pc: pc.category.name, pc_list)))


# ===============================================
# рассылка нового сообщения
# ===============================================
def mailing_new_post(post_id):

    # получить пост
    post = Post.objects.get(id=post_id)

    # получить список подписчиков
    subscribers = []
    # для всех м2м, где есть этот пост
    for pc in PostCategory.objects.filter(post=post):
        # получить подписчиков для этой категории
        subscribers = SubscriberCategory.objects.filter(category=pc.category)
    # отфильтровать одинаковые
    subscribers = list(set(subscribers))

    # есть подписчики
    if subscribers:
        # сформировать текст сообщения
        text = ' '.join(post.text.split()[:MAIL_TEXT_LIMIT]) + '...'  # ограничить длину текста

        # для каждого подписчика
        for subscriber in subscribers:
            # сформировать html текст формы email_created.html с заполненными полями
            html_content = render_to_string('news/email_created.html', {'title': post.title,
                                                                        'text': text,
                                                                        'post_id': post.id})
            # сформировать сообщение
            msg = EmailMultiAlternatives(
                subject=f'Здравствуйте, {subscriber.subscriber.user.username}. новая статья в Вашем любимом разделе!',
                body=text,
                from_email=os.getenv("EMAIL_ADDRESS"),
                to=[subscriber.subscriber.user.email, ],
            )
            # отправить сообщение
            msg.attach_alternative(html_content, "text/html")
            # TODO uncomment for work
            # msg.send()
            logger.debug(f'user: {subscriber.subscriber.user.username}, email: {subscriber.subscriber.user.email}')


# ===============================================
# еженедельный отчет о новых постах
# ===============================================
def mailing_week_report():
    # для каждого подписчика
    for subscriber in Subscriber.objects.all():
        pc_list = []
        # для каждой подписной категории подписчика
        for sc in SubscriberCategory.objects.filter(subscriber=subscriber):
            # получить список постов
            for pc in PostCategory.objects.filter(category=sc.category):
                # отобрать те, которые старше 7 дней
                if pc.post.time_in.date() > datetime.date.today() - datetime.timedelta(days=MAILING_DAYS):
                    # отфильтровать собственные посты
                    if pc.user.email != subscriber.user.email:
                        pc_list.append(pc)

        # есть посты в списке
        if pc_list:
            # сформировать html текст формы email_sender.html с заполненными полями
            html_content = render_to_string('news/email_sender.html', {'pc_list': pc_list})

            # сформировать сообщение
            msg = EmailMultiAlternatives(
                subject=f'Здравствуйте, {subscriber.user.username}!',
                body='ok',
                from_email=os.getenv("EMAIL_ADDRESS"),
                to=[subscriber.user.email, ],
            )

            # отправить сообщение
            msg.attach_alternative(html_content, "text/html")
            # TODO uncomment for work
            # msg.send()
            logger.debug(f'user: {subscriber.subscriber.user.username}, email: {subscriber.subscriber.user.email}')
