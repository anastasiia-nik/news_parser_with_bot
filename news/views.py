from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from news.forms import CommentForm
from news.models import Category, News, Tags


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
        comments = article.comments.filter(approved=True)
        new_comment = None

        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.news_id = article
                new_comment.save()
        else:
            comment_form = CommentForm()

        context = {
            'article': article,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form
        }

    except News.DoesNotExist:
        raise Http404("Article does not exist")

    return render(request, 'article_view.html', context=context)




def tag(request, tag_name=None):
    try:
        t = Tags.objects.get(tag=tag_name)
        news_in_tag = News.objects.filter(tags=t)
        context = {'news_in_tag': news_in_tag}
    except Tags.DoesNotExist:
        raise Http404("Tag does not exist")
    return render(request, 'tag.html', context=context)
