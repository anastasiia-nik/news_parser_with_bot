from .models import Category, Tags


def all_categories(request):
    return {'categories_list': Category.objects.all()}

def all_tags(request):
    return {'tags_list': Tags.objects.all()}