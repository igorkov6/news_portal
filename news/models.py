# news/models.py
# ===============================================
# модели
# ===============================================

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache
from loguru import logger


# ===============================================
# Автор поста
# ===============================================
class Author(models.Model):

    # Пользователь из встроенной модели. связь - "один к одному"
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # рейтинг автора
    rating = models.IntegerField(default=0)

    # обновление рейтинга автора
    def update_rating(self, rating):
        self.rating = rating

    # печать автора
    def __str__(self):
        return self.user.username.title()


# ===============================================
# Категория постов - темы, которые они отражают
# ===============================================
class Category(models.Model):

    # название категории - спорт, политика, и т.д.
    name = models.CharField(max_length=255, unique=True)

    # печать категории
    def __str__(self):
        return self.name.title()


# ===============================================
# Модель поста
# ===============================================
class Post(models.Model):

    # Автор поста. связь - "один к многим"
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)

    # признак поста - новость / статья
    isNews = models.BooleanField(default=True)

    # Дата создания поста. Добавляется автоматически.
    time_in = models.DateTimeField(auto_now_add=True)

    # Категория поста. Связь - "многие ко многим"
    category = models.ManyToManyField(Category, through='PostCategory', null=False)

    # заголовок поста
    title = models.CharField(max_length=255, null=False)

    # текст поста
    text = models.TextField(null=False)

    # рейтинг поста
    rating = models.IntegerField(default=0)

    # лайк - увеличение рейтинга поста
    def like(self):
        self.rating += 1
        self.save()

    # дизлайк - уменьшение рейтинга поста
    def dislike(self):
        self.rating -= 1
        self.save()

    # предварительный просмотр поста
    def preview(self):
        return self.text[:124] + '...'

    # страница возврата после создания и редактирования
    def get_absolute_url(self):
        return reverse('post_new_url', args=[str(self.id)])

    # переопределяем метод сохранения
    def save(self, *args, **kwargs):

        # сначала вызываем метод родителя, чтобы объект сохранился
        super().save(*args, **kwargs)
        logger.debug(f'save to db: {self.pk}')

        # затем удаляем его из кэша, чтобы сбросить его
        cache.delete(f'post-{self.pk}')
        logger.debug(f'post del from cache: {self.pk}')


# ===============================================
# промежуточная модель для связи "многие ко многим"
# ===============================================
class PostCategory(models.Model):

    # Пост. Связь - "один ко многим"
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)

    # Категория. Связь - "один ко многим"
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)


# ===============================================
# Комментарий к посту.
# ===============================================
class Comment(models.Model):

    # Пост, к которому относится комментарий. Связь - "один ко многим"
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)

    # Пользователь, который оставил комментарий. Связь - "один ко многим"
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    # текс комментария
    text = models.TextField(null=False)

    # дата создания комментария
    date_in = models.DateTimeField(auto_now_add=True)

    # рейтинг комментария
    rating = models.IntegerField(default=0)

    # лайк - увеличение рейтинга комментария
    def like(self):
        self.rating += 1

    # дизлайк - уменьшение рейтинга комментария
    def dislike(self):
        self.rating -= 1


# ===============================================
# подписчик
# ===============================================
class Subscriber(models.Model):

    # пользователь - подписчик
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # категории подписчика
    category = models.ManyToManyField(Category, through='SubscriberCategory', null=False)


# ===============================================
# промежуточная модель для связи "многие ко многим"
# ===============================================
class SubscriberCategory(models.Model):

    # Подписчик. Связь - "один ко многим"
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, null=False)

    # Категория. Связь - "один ко многим"
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)