from django.urls import path, re_path

from rest_framework import routers

from news import views
from news.views import NewsViewSet, TagsViewSet

router = routers.DefaultRouter()
router.register(r'news', NewsViewSet)
router.register(r'tag', TagsViewSet)
# router.register(r'tag/<str:tag_name>/', NewsViewSet)
# # re_path('api/tags/(?P<tagname>.+)/$', TagsViewSet.as_view()),
#
#
# urlpatterns = [
#     path('api/news/tag/<str:tag_name>', views.newsapi_tag, name='newsapi_tag'),
#
# ]