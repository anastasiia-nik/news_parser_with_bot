from .models import Category, Tags, News


def all_categories(request):
    return {'categories_list': Category.objects.all()}

def all_tags(request):
    tags_list = []
    tags_list_temp = Tags.objects.all()
    news_list = News.objects.all()
    for tag in tags_list_temp:
        tags_list.append([tag, news_list.filter(tags=tag).count()])



    # (sorted(C, key=lambda x: x[0], reverse=True)))
    return {'tags_list': sorted(tags_list, key= lambda x:x[1], reverse=True)}


    def counter(self):
        return News.objects.filter(tags=self).count()