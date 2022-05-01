from django.contrib import admin

from news.models import Author, Category, Tags, News

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(News)

# Register your models here.
