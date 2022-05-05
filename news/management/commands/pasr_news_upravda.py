import news.parsers.news_pars2 as pu
from django.core.management.base import BaseCommand, CommandError
import news.models as nm


class Command(BaseCommand):

    def handle(self, *args, **options):
        upravda = pu.Upravda()
        upravda.parse_all()
        self.add_authors(upravda)
        self.add_tags(upravda)
        self.add_news(upravda)

    def add_authors(self, parser: pu.Upravda):
        authors_list = []
        for news in parser.all_news:
            authors_list.append(news.news_author)
        authors_set = set(authors_list)
        authors_from_db = nm.Author.objects.all()
        authors_list_from_db = []
        # for author in authors_from_db:
        #     authors_list_from_db.append(author)
        # authors_set_from_db = set(authors_list_from_db)
        authors_set_from_db = set(author.name for author in authors_from_db)
        unique_authors = authors_set - authors_set_from_db
        for author in unique_authors:
            nm.Author.objects.create(name=author)

    def add_tags(self, parser: pu.Upravda):
        tags_list = []
        for news in parser.all_news:
            tags_list += news.news_tags
        tags_set = set(tags_list)
        tags_from_db = nm.Tags.objects.all()
        tags_set_from_db = set(tag.tag for tag in tags_from_db)
        unique_tags = tags_set - tags_set_from_db
        for tag in unique_tags:
            nm.Tags.objects.create(tag=tag)

    def add_news(self, parser: pu.Upravda):
        news_list = []
        for news in parser.all_news:
            news_list.append(news.news_title)
        news_set = set(news_list)
        news_from_db = nm.News.objects.all()
        # tags_list_from_db = []
        news_set_from_db = set(news.title for news in news_from_db)
        unique_news = news_set - news_set_from_db
        tags_from_db = nm.Tags.objects.all()
        authors_from_db = nm.Author.objects.all()
        for news in parser.all_news:
            if news.news_title in unique_news:
                author_current = authors_from_db.get(name=news.news_author)
                try:
                    category_current = nm.Category.objects.get(name='upravda')
                except:
                    category_current = nm.Category.objects.create(name='upravda')
                tags_current_ids = []
                for tag in news.news_tags:
                    tags_current_ids.append(tags_from_db.get(tag=tag).id)
                news_object = nm.News.objects.create(title=news.news_title,
                                                     date=news.news_data,
                                                     text=news.news_text,
                                                     author=author_current,
                                                     category=category_current,
                                                     image=news.news_photo)
                news_object.tags.add(*tags_current_ids)
                news_object.save()


    # news_title: str
    # news_author: str
    # news_data: datetime
    # news_text: str
    # news_photo: str
    # news_tags: [str]
    # title = models.CharField(max_length=500)
    # date = models.DateTimeField(blank=True, null=True)
    # text = models.TextField()
    # category = models.ForeignKey(Category, on_delete=models.PROTECT)
    # author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    # tags = models.ManyToManyField(Tags, blank=True)
    # image = models.ImageField(upload_to='news/images/', blank=True, null=True)
