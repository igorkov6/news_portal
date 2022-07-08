# news/admin.py

from django.contrib import admin
from .models import Category, PostCategory, Post, Author, Comment, Subscriber, SubscriberCategory

# ===============================================
# регистрация моделей
# ===============================================
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Subscriber)
admin.site.register(SubscriberCategory)
