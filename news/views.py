# news/views.py
# ===============================================
# представления
# ===============================================

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .models import Post, Author, PostCategory, Subscriber, SubscriberCategory
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from .forms import PostForm, ProfileForm, SubscriberForm
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .filters import PostFilterForm
from loguru import logger
from .settings import *
import datetime
from .utils import get_category_list
from django.core.cache import cache


# ===============================================
# поиск постов
# ===============================================
class PostSearchView(PermissionRequiredMixin, ListView):
    permission_required = ('news.view_post',)

    filter_set = None

    # модель, объекты которой будем выводить
    model = Post

    # поле объекта Post, по которому выполняется сортировка
    ordering = '-time_in'

    # шаблон страницы вывода постов
    template_name = 'news/post_search.html'

    # имя, по которому обращаемся к объекту из шаблона
    context_object_name = 'post_list'

    # количество записей на странице
    paginate_by = 10

    # переопределить функцию получения списка новостей
    def get_queryset(self):
        # получить полный набор постов
        query_set = super().get_queryset()

        # получить запрос фильтрации
        get_request = self.request.GET

        # получить набор фильтров формы согласно запросу
        self.filter_set = PostFilterForm(get_request, query_set)

        # возвратить набор постов согласно фильтру
        return self.filter_set.qs

    # изменить контекст формы
    def get_context_data(self, **kwargs):
        # получить весь контекст
        context = super().get_context_data(**kwargs)

        # добавить набор фильтров в контекст для отображения
        context['filterset'] = self.filter_set
        context['section'] = 'search'

        # возвратить контекст
        return context


# ===============================================
# список постов
# ===============================================
class PostListView(PermissionRequiredMixin, ListView):
    permission_required = ('news.view_post',)

    # модель, объекты которой будем выводить
    model = Post

    # поле объекта Post, по которому выполняется сортировка
    ordering = '-time_in'

    # шаблон вывода постов
    template_name = 'news/post_main.html'

    # имя, по которому обращаемся к объекту из шаблона
    context_object_name = 'post_list'

    # количество записей на странице
    paginate_by = 10

    # изменить контекст формы
    def get_context_data(self, **kwargs):
        # получить весь контекст
        context = super().get_context_data(**kwargs)
        context['section'] = 'news'
        # возвратить контекст
        return context


# ===============================================
# отображение одного поста
# ===============================================
class PostDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ('news.view_post', )

    # вид поста
    mode = 'view'

    # модель поста
    model = Post

    # имя, по которому обращаемся к посту из шаблона
    context_object_name = 'post'

    # шаблон поста
    template_name = 'news/post_detail.html'

    # получить все посты
    queryset = Post.objects.all()

    # получить запрашиваемый пост
    def get_object(self, *args, **kwargs):

        # получить из кэша
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        # не в кэше
        if not obj:

            # получить из базы
            obj = super().get_object(queryset=self.queryset)
            logger.debug(f'post get from db: {self.kwargs["pk"]}')

            # сохранить в кэше
            cache.set(f'post-{self.kwargs["pk"]}', obj)
            logger.debug(f'post set to cache: {self.kwargs["pk"]}')

        else:
            logger.debug(f'post get from cache: {self.kwargs["pk"]}')

        # возвратить пост
        return obj

    # удаление
    if mode == 'delete':
        # адрес возврата после удаления
        success_url = reverse_lazy('post_list_url')

    # остальные режимы
    else:
        # для старых постов
        if mode == 'view':

            # обработка запроса post
            def post(self, request, *args, **kwargs):

                # получить пост
                post_id = self.request.path.split('/')[-3]
                post = Post.objects.get(id=post_id)

                # лайк
                if 'like' in self.request.POST:
                    post.like()

                # дизлайк
                if 'dislike' in self.request.POST:
                    post.dislike()

                # нажата кнопка Подписаться
                if 'subscribe' in self.request.POST:

                    # если пользователь не подписчик
                    if not Subscriber.objects.filter(user=self.request.user).exists():
                        # сделать пользователя подписчиком
                        subs = Subscriber.objects.create(user=self.request.user)
                        subs.save()

                    # получить подписчика
                    subscriber = Subscriber.objects.get(user=self.request.user)

                    # получить список категорий
                    pc_list = PostCategory.objects.filter(post=post)

                    # подписаться на категории по списку
                    for pc in pc_list:
                        # если такой подписки еще нет
                        if not SubscriberCategory.objects.filter(subscriber=subscriber, category=pc.category).exists():
                            # создать подписку
                            sc = SubscriberCategory.objects.create(subscriber=subscriber, category=pc.category)
                            sc.save()

                return redirect(self.request.path, {'context': 'ok'})

        # изменить контекст формы
        def get_context_data(self, **kwargs):

            # получить весь контекст
            context = super().get_context_data(**kwargs)

            # получить идентификатор поста
            post_id = int(self.request.path.split('/')[-3])

            # получить список тем
            context['cats'] = get_category_list(post_id)

            # вид поста
            context['post_mode'] = self.mode

            # возвратить контекст
            return context


# ===============================================
# создать пост
# ===============================================
class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)

    # форма поста
    form_class = PostForm

    # модель поста
    model = Post

    # вид поста
    isNews = False

    # имя, по которому обращаемся к посту из шаблона
    context_object_name = 'post'

    # шаблон редактора новости
    template_name = 'news/post_create.html'

    # изменить контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_news'] = self.isNews
        context['section'] = 'create'
        return context

    # переопределение метода
    # определение автора и признака новости
    def form_valid(self, form):

        # получить не сохраненные данные формы
        post = form.save(commit=False)
        author = Author.objects.get(user=self.request.user)

        # определить количество постов автора за сегодняшний день
        x = 0
        for p in Post.objects.filter(author=author):
            if p.time_in.date() == datetime.date.today():
                x += 1

        # превышен лимит постов
        if x > ONE_DAY_POST_CREATE_LIMIT:
            return redirect('/post_limit/')

        # изменить данные формы
        post.isNews = self.isNews
        post.author = author

        # возврат с сохранением данных формы
        return super().form_valid(form)


# ===============================================
# редактор поста
# ===============================================
class PostEditView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)

    # форма поста
    form_class = PostForm

    # модель поста
    model = Post

    # вид поста
    isNews = False

    # имя, по которому обращаемся к посту из шаблона
    context_object_name = 'post'

    # шаблон редактора поста
    template_name = 'news/post_edit.html'

    # изменить контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_news'] = self.isNews
        return context


# ===============================================
# редактор профайла текущего пользователя
# ===============================================
class ProfileEditView(LoginRequiredMixin, UpdateView):
    # модель пользователя
    model = User

    # форма редактора
    form_class = ProfileForm

    # шаблон редактора
    template_name = 'accounts/profile.html'

    # путь перехода после завершения редактирования
    success_url = '/news/'

    # получить текущего пользователя
    def get_object(self, queryset=None):
        return self.request.user

    # изменить контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # передать в контекст формы сведения о том, является ли пользователь автором
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()

        # если пользователь не подписчик
        if not Subscriber.objects.filter(user=self.request.user).exists():
            # сделать пользователя подписчиком
            subs = Subscriber.objects.create(user=self.request.user)
            subs.save()

        context['section'] = 'profile'

        return context

    def form_valid(self, form):

        # стать автором
        if 'auth' in self.request.POST:
            return redirect('/news/make_author')

        # управление подпиской
        if 'subs' in self.request.POST:
            return redirect('/news/edit_subscriber')

        # возврат с сохранением данных формы
        return super().form_valid(form)


# ===============================================
# редактор подписки
# ===============================================
class SubscriberEditView(LoginRequiredMixin, UpdateView):
    # модель пользователя
    model = Subscriber

    # форма редактора
    form_class = SubscriberForm

    # шаблон редактора
    template_name = 'accounts/edit_subscriber.html'

    # путь перехода после завершения редактирования
    success_url = '/news/'

    # получить текущего пользователя
    def get_object(self, queryset=None):
        user = self.request.user
        subs = Subscriber.objects.get(user=user)
        return subs

    def form_valid(self, form):

        logger.debug(self.request.POST)

        # управление подпиской
        if 'subs' in self.request.POST:
            return redirect('/news/del_subscriber')

        # возврат с сохранением данных формы
        return super().form_valid(form)


# ===============================================
# страница приветствия после входа
# ===============================================
@login_required
def news_login_view(request):
    return redirect('/login_page/')


# ===============================================
# стать автором
# ===============================================
@login_required
def make_author_view(request):
    # получить пользователя
    user = request.user

    # получить группу авторов
    authors_group = Group.objects.get(name='authors')

    # если пользователя еще нет в этой группе
    if not request.user.groups.filter(name='authors').exists():
        # добавить
        authors_group.user_set.add(user)

    # если пользователь не является автором
    if not Author.objects.filter(user=user).exists():
        # создать такого автора
        aut = Author.objects.create(user=user, rating=0)
        aut.save()

    # загрузить шаблон
    return redirect('/author/')


# ===============================================
# удалить подписку
# ===============================================
@login_required
def del_subscriber_view(request):
    # получить пользователя
    user = request.user

    # если пользователь еще подписчик
    if Subscriber.objects.filter(user=user).exists():
        # удалить подписчика
        Subscriber.objects.filter(user=user).delete()

    # загрузить шаблон
    return redirect('/unsubscribe/')
