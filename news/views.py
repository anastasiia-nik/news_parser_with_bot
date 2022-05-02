from django.http import Http404
from django.shortcuts import render

from news.models import Category, News

# Create your views here.
def main_page(request):
    news_list = News.objects.order_by('-id').all()
    context = {'news_list': news_list}
    return render(request, 'new_index.html', context=context)

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
    return render(request, 'category.html', context=context)

