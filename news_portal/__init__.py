# __init__.py

# это позволяет убедиться,
# что приложение всегда импортируется,
# когда запускается django
from .celery import app as celery_app

__all__ = ('celery_app',)
