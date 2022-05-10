from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from news import views

urlpatterns = [
    path('', views.main_page, name='home'),
    path('category_<str:cat_name>/', views.category, name='category_name'),
    path('tag_<str:tag_name>/', views.tag, name='tag_name'),
    path('article_<str:article_name>', views.show_article, name='article_name'),
    path('subscribe/', views.subscribe, name='subscribe'),

    path('api/news/<int:pk>', views.newsapi, name='newsapi'),
]
