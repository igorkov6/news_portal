# news/apps.py
# ===============================================
# конфигурация приложения
# ===============================================

from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    # подгрузка сигналов при старте приложения
    def ready(self):
        import news.signals
