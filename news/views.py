from django.http import Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from news.forms import SubscribeForm, ContactForm
from news.models import Category, News, Tags, Subscribers


@csrf_exempt
def subscribe(request):
    news_list = News.objects.all().order_by('-id')
    if 'q' in request.GET:
        news_list = news_list.filter(title__icontains=request.GET['q'])


    form = SubscribeForm()
    f2 = ContactForm()
    if request.method == 'POST':
        form = SubscribeForm(data=request.POST)
        if form.is_valid():
            instance = form.save(False)
            last_id = 0
            if News.objects.all().exists():
                last_id = News.objects.order_by('-id').first().id
            instance.last_news_id = last_id
            instance.save()


    context = {'news_list': news_list, 'top_news': news_list.first(), 'subscribe_form': form, 'contact_form': f2}
    return render(request, 'new_index.html', context=context)

# Create your views here.
def main_page(request):
    news_list = News.objects.all().order_by('-id')
    context = {'news_list': news_list, 'top_news': news_list.first()}
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

def show_article(request, article_name=None):
    try:
        article = News.objects.get(title=article_name)
        context = {'article': article}
    except News.DoesNotExist:
        raise Http404("Article does not exist")
    return render(request, 'new_view.html', context=context)



def tag(request, tag_name=None):
    try:
        t = Tags.objects.get(tag=tag_name)
        news_in_tag = News.objects.filter(tags=t)
        context = {'news_in_tag': news_in_tag}
    except Tags.DoesNotExist:
        raise Http404("Tag does not exist")
    return render(request, 'tag.html', context=context)