from django.shortcuts import render

from news.models import Category, News

# Create your views here.
def main_page(request):
    categories_list = Category.objects.all()
    news_list = News.objects.order_by('-id').all()
    context = {'categories_list': categories_list, 'news_list': news_list}
    return render(request, 'index.html', context=context)


