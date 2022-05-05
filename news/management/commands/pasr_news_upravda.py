import news.parsers.news_pars2 as pu
from django.core.management.base import BaseCommand, CommandError
import news.models as nm


class Command(BaseCommand):

    def handle(self, *args, **options):
        upravda = pu.Upravda()
        upravda.parse_all()
        self.add_tags(upravda)
        self.add_news(upravda)

    def add_authors(self, parser: pu.Upravda):
        nm.Author.objects.bulk_create([nm.Author(name=news.news_author) for news in parser.all_news],
                                      ignore_conflicts=True)

    def add_tags(self, parser: pu.Upravda):
        tags = set()
        for news in parser.all_news:
            tags.update(set(news.news_tags))
        nm.Tags.objects.bulk_create([nm.Tags(tag=tag) for tag in tags], ignore_conflicts=True)

    def add_news(self, parser: pu.Upravda):
        for news in parser.all_news:
            author_current, _ = nm.Author.objects.get_or_create(name=news.news_author,)
            category_current, _ = nm.Category.objects.get_or_create(name='upravda')
            news_tags = nm.Tags.objects.filter(tag__in=news.news_tags)
            news, _ = nm.News.objects.get_or_create(
                title=news.news_title, defaults={'date': news.news_data, 'text': news.news_text,
                                                 'author': author_current, 'category': category_current,
                                                 'image': news.news_photo})
            news.tags.clear()
            news.tags.add(*news_tags)


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
