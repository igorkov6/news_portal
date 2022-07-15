# articles_urls.py
# ===============================================
# пути статей - article/
# ===============================================

from django.urls import path
from .views import PostEditView, PostDeleteView, PostCreateView

urlpatterns = [

    # создать новость
    path('create/', PostCreateView.as_view(isNews=False)),

    # редактор новости
    path('<int:pk>/edit/', PostEditView.as_view(isNews=False)),

    # удалить новость
    path('<int:pk>/delete/', PostDeleteView.as_view()),
]
