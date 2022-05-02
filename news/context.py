from .models import Category

def all_categories(request):
    return {'categories_list': Category.objects.all()}