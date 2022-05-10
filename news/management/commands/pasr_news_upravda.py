import news.parsers.news_pars2 as pu
from django.core.management.base import BaseCommand, CommandError
import news.models as nm
from news.parsers.apply_pars import apply_pars


class Command(BaseCommand):

    def handle(self, *args, **options):
        # upravda = pu.Upravda()
        # upravda.parse_all()
        # self.add_tags(upravda)
        # self.add_news(upravda)
        apply_pars()




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
