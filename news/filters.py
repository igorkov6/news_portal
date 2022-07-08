# news/filters.py
# ===============================================
# фильтры
# ===============================================

import django_filters
from django_filters import FilterSet
from django import forms
from .models import Post


# ===============================================
# фильтр поиска постов по критериям
# ===============================================
class PostFilterForm(FilterSet):

    # поле времени определяем самостоятельно,
    # так как использован специальный виджет date
    time_in = django_filters.DateFilter(
        lookup_expr='gt',
        widget=forms.DateInput(attrs={'type': 'date',})
    )

    # остальные поля поиска формируем средствами django
    class Meta:

        model = Post

        fields = {
            'title': ['icontains'],
            'text': ['icontains'],
        }
