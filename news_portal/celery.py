# news_portal/celery.py
# ===============================================
# конфигурация celery
# ===============================================

import os
from celery import Celery
from celery.schedules import crontab

# это код скопирован с manage.py
# он установит модуль настроек по умолчанию django для приложения 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')

# создаем экземпляр приложения Celery
app = Celery('news_portal')

# Для получения настроек django, связываем префикс 'CELERY' с настройкой celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# загрузка tasks.py в приложение django
app.autodiscover_tasks()

# планировщик запускает задачу по расписанию
app.conf.beat_schedule = {

    # имя периодического задания
    'mail_report': {

        # расписание периодического запуска задачи
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),

        # задача, запускаемая по этому расписанию
        'task': 'news.tasks.mail_report',

        # аргументы, передаваемые в эту задачу
        'args': (),
    },
}
