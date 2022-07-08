# views/urls.py
# ===============================================
# пути
# ===============================================

from django.urls import path
from .views import PostListView, PostDetailView, PostSearchView, PostEditView
from .views import ProfileEditView, make_author_view, news_login_view
from .views import del_subscriber_view, SubscriberEditView, PostCreateView
from django.contrib.auth.views import LogoutView
from django.views.decorators.cache import cache_page

# ===============================================
# пути страницы news
# ===============================================
urlpatterns = [

    # все посты кэширование 1 минута
    path('', cache_page(60)(PostListView.as_view()), name='post_list_url'),

    # поиск поста
    path('search/', PostSearchView.as_view()),

    # создать пост
    path('create/', PostCreateView.as_view(isNews=True)),

    # новый пост
    path('<int:pk>/new/', PostDetailView.as_view(mode='new'), name='post_new_url'),

    # просмотр поста
    path('<int:pk>/view/', PostDetailView.as_view(mode='view')),

    # удалить пост
    path('<int:pk>/delete/', PostDetailView.as_view(mode='delete')),

    # редактор поста
    path('<int:pk>/edit/', PostEditView.as_view(isNews=True)),

    # вход пользователя
    path('login/', news_login_view, name='login_url'),

    # выход пользователя
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout_url'),

    # редактор профиля
    path('profile/', ProfileEditView.as_view(), name='profile_url'),

    # стать автором
    path('make_author/', make_author_view),

    # удалить подписку
    path('del_subscriber/', del_subscriber_view),

    # стать подписчиком
    path('edit_subscriber/', SubscriberEditView.as_view(), name='edit_subscriber'),
]
