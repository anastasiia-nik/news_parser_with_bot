from functools import wraps
from django.core.cache import cache
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets

from news.forms import CommentForm, Comment2Form
from news.models import Category, News, Tags
# Create your views here.
from news.serializer import NewsShortSerializer, NewsFullSerializer
from news.tasks import store_comment


def main_page(request):
    news_list = News.objects.all().order_by('-date')
    context = {'news_list': news_list, 'top_news': news_list.first()}
    return render(request, 'new_index.html', context=context)


def newsapi(request, pk=None):
    if request.method == 'GET':
        return JsonResponse(NewsShortSerializer(News.objects.all()[:5], many=True).data, safe=False)

    if request.method == 'POST' and request.user.is_superuser:
        pass
    if request.method == 'DELETE' and request.user.is_superuser and pk:
        News.objects.filter(pk=pk).delete()


# def news_page(request):
#     categories_list = Category.objects.all()
#     news_list = News.objects.order_by('-id').all()
#     context = {'categories_list': categories_list, 'news_list': news_list}
#     return render(request, 'new_index.html', context=context)

def category(request, cat_name=None):
    try:
        c = Category.objects.get(name=cat_name)
        news_in_cat = News.objects.filter(category=c)
        context = {'news_in_cat': news_in_cat}
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    return JsonResponse({
        'success': True, 'data': ['123', '4232']
    })
    return JsonResponse({
        'status': True, 'data': ['123', '4232']
    })
    return JsonResponse({
        'success': 'ok', 'data': ['123', '4232']
    })
    return render(request, 'category.html', context=context)


def show_article(request, slug=None):
    article = get_object_or_404(News, slug=slug)
    new_comment = None

    if request.method == 'POST':
        comment_form = Comment2Form(data=request.POST, context={'request': request, 'article': article})
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            store_comment.delay(
                data['author'], data['text'], article.pk
            )
            new_comment = True
            # new_comment = comment_form.save(commit=False)
            # new_comment.news_id = article
            # new_comment.save()
        else:
            print(comment_form.errors)
    else:
        comment_form = CommentForm()

    context = {
        'article': article,
        'comments': article.public_comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    }

    return render(request, 'article_view.html', context=context)


def tag(request, tag_name=None):
    try:
        t = Tags.objects.get(tag=tag_name)
        news_in_tag = News.objects.filter(tags=t)
        context = {'news_in_tag': news_in_tag}
    except Tags.DoesNotExist:
        raise Http404("Tag does not exist")
    return render(request, 'tag.html', context=context)


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsShortSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return NewsShortSerializer
        return NewsFullSerializer

# class TagsViewSet(viewsets.ModelViewSet):
#     queryset = News.objects.filter()
#     serializer_class = TagSerializer

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return NewsShortSerializer
    #     return NewsFullSerializer