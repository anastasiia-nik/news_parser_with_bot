from django.core.management import BaseCommand
from functools import wraps
from news.models import News


class Command(BaseCommand):

    def handle(self, *args, **options):
        def decor1(func):
            print("RUN DECOR1 ", func.__name__)

            def wrapper1(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper1

        def decor2(func):
            print("RUN DECOR2 ", func.__name__)
            qq = {}
            @wraps(func)
            def wrapper2(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper2

        @decor1
        @decor2
        def hello():
            return "Hello world"

        print(hello)
        print(hello())
        return
        all_news = News.objects.all()
        for article in all_news:
            article.save()