"""demo URL Configuration

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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from news import views
from news.router import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='home'),
    path('', views.main_page, name='subscribe'),
    path('category_<str:cat_name>/', views.category, name='category_name'),
    path('tag_<str:tag_name>/', views.tag, name='tag_name'),
    path('article_<str:slug>', views.show_article, name='article_name'),
    # path('add_comment/>', views.add_comment, name='comment')
    path('qwesgfgsd34254141akfuhkajdf/', views.newsapi, name='newsapi'),
    path("api/", include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),

    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    path('docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
