"""news_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

# пути страниц
urlpatterns = [

    # админка
    path('admin/', admin.site.urls),

    # страница новостей - пути в файле news/urls.py
    path('news/', include('news.urls')),

    # страница новостей - пути в файле news/urls.py
    path('', include('news.urls')),

    # страница статей - пути в файле news/articles_urls.py
    path('article/', include('news.articles_urls')),

    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('assets/favicon.ico'))),

    path('accounts/', include('accounts.urls')),

    path('account/', include('allauth.urls')),

    path('pages/', include('django.contrib.flatpages.urls')),
]
