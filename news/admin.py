from django.contrib import admin

from news.models import Author, Category, Tags, News, Comment, LastSendedNews

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(News)
admin.site.register(LastSendedNews)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'news_id', 'date', 'approved')
    list_filter = ('approved', 'date')
    search_fields = ('author', 'text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

# Register your models here.
