from django.core.management import BaseCommand

from news.models import News


class Command(BaseCommand):

    def handle(self, *args, **options):
        all_news = News.objects.all()
        for article in all_news:
            article.save()