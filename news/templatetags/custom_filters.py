# ===============================================
# собственные фильтры
# ===============================================

from django import template
from ..models import *

register = template.Library()


# ===============================================
# фильтр цензора
# ===============================================
@register.filter()
def censor_filter(value):

    # получить список из строки
    text_list = value.split()

    # для каждого слова
    for index, word in enumerate(text_list):

        # если слово начинается с заглавной буквы
        if len(word) > 1 and word.isalpha() and word == word.capitalize():

            # заменить буквы слова звездочкой
            text_list[index] = word[0] + ('*' * (len(word) - 1))

    # собрать строку
    return ' '.join(text_list)


# ===============================================
# фильтр определения количества новостей в базе
# ===============================================
@register.filter()
def news_number_filter(obj):
    return len(Post.objects.filter(isNews=True))


# ===============================================
# фильтр определения количества статей в базе
# ===============================================
@register.filter()
def article_number_filter(obj):
    return len(Post.objects.filter(isNews=False))
