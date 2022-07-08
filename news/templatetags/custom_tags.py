# ===============================================
# собственные теги
# ===============================================

from datetime import datetime
from django import template
from ..models import *

register = template.Library()


# ===============================================
# тег определения общего количества постов
# ===============================================
@register.simple_tag()
def post_number_tag():
    return len(Post.objects.all())


# ===============================================
# тег определения общего количества новостей
# ===============================================
@register.simple_tag()
def news_number_tag():
    return len(Post.objects.filter(isNews=True))


# ===============================================
# тег определения общего количества статей
# ===============================================
@register.simple_tag()
def article_number_tag():
    return len(Post.objects.filter(isNews=False))


# ===============================================
# тег вывода текущей даты
# ===============================================
@register.simple_tag()
def current_time_tag(format_string='%d %b %Y'):
    return datetime.utcnow().strftime(format_string)


# ===============================================
# тег коррекции get запроса
# ===============================================
@register.simple_tag(takes_context=True)
def url_replace_tag(context, **kwargs):

    # получить все параметры текущего запроса
    d = context['request'].GET.copy()

    # изменить параметры на новые значения
    for k, v in kwargs.items():
        d[k] = v

    # возвратить текущий запрос
    return d.urlencode()
