# news/forms.py
# ===============================================
# формы
# ===============================================

from django import forms
from .models import Post, Subscriber
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# ===============================================
# форма ввода / редактирования поста
# ===============================================
class PostForm(forms.ModelForm):

    class Meta:

        # модель, из которой форма тянет данные
        model = Post

        # поля данных, вытянутых из модели
        fields = [
            # 'author',
            'category',
            'title',
            'text'
        ]

    # валидатор данных
    def clean(self):

        # получить все параметры формы
        cleaned_data = super().clean()

        # получить контролируемые параметры
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')

        # одинаковый текст
        if title == text:
            raise ValidationError("Текст должен отличаться от заголовка")

        # если меньше 5 слов
        if len(text.split()) < 5:
            raise ValidationError("Слишком короткий текст")

        # возврат всех данных формы
        return cleaned_data


# ===============================================
# форма ввода / редактирования профиля
# ===============================================
class ProfileForm(forms.ModelForm):

    class Meta:

        # модель, из которой форма тянет данные
        model = User

        # поля данных, вытянутых из модели
        fields = [
            'username',
            'first_name',
            'last_name',
            'email'
        ]


class SubscriberForm(forms.ModelForm):

    class Meta:

        # модель, из которой форма тянет данные
        model = Subscriber

        # поля данных, вытянутых из модели
        fields = [
            'category',
        ]