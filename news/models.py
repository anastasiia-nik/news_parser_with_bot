from datetime import datetime
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.cache import cache
from django.db import models
from django.core.validators import MinLengthValidator


class Author(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    @property
    def has_news(self) -> bool:
        return News.objects.filter(category=self).exists()

    def __str__(self):
        return self.name


class Tags(models.Model):
    tag = models.CharField(max_length=100, unique=True)

    @property
    def has_news(self) -> bool:
        return News.objects.filter(tags=self).exists()

    @property
    def counter(self):
        return News.objects.filter(tags=self).count()

    # @classmethod
    # def get_popular_tags(cls):
    #     tag_dict = {}
    #     for tag in cls.objects.all():
    #         tag_dict[tag] = News.objects.filter(tags=tag).count()
    #     tag_dict_sorted = {dict(sorted(tag_dict.items(), key=lambda item: item[1]))}
    #     list_tag = [tag_dict_sorted[i] for i in range(0,10)]
    #     print(list_tag)

    def __str__(self):
        return self.tag


class News(models.Model):
    cache_comment_timeout_sec = 3600

    title = models.CharField(max_length=500)
    date = models.DateTimeField(blank=True, null=True)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    image = models.ImageField(upload_to='news/images/', blank=True, null=True)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    @property
    def comment_counter(self):
        cache_key = self.comment_counter_cache_key(self.pk)
        data = cache.get(cache_key)
        if data is not None:

            return data
        print(f"{cache_key} store for {self.pk}")
        one_news = News.objects.get(id=self.id)
        data = one_news.comments.filter(approved=True).count()
        cache.set(cache_key, data, self.cache_comment_timeout_sec)
        return data

    @classmethod
    def comment_counter_cache_key(cls, news_id):
        return f"{news_id}_cache_comment"

    @property
    def public_comments(self):
        return self.comments.filter(approved=True)


class Comment(models.Model):
    author = models.CharField(max_length=150, validators=[MinLengthValidator(2)])
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    news_id = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']
        unique_together = (('author', 'text'),)

    def __str__(self):
        return 'Comment {} by {}'.format(self.text, self.author)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):

        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    @classmethod
    def last_comments(cls):
        return cls.objects.filter(approved=True).order_by('-date')[:5]


@receiver(post_save, sender=Comment)
def post_save_handler(sender,instance=None, created=False, **kwargs):
    instance: Comment
    cache_key = News.comment_counter_cache_key(instance.id)
    cache.delete(cache_key)


class Subscriber(models.Model):
    chat_id = models.CharField(unique=True, max_length=150)


class LastSendedNews(models.Model):
    news_id = models.IntegerField(unique=True)
    # last_news_id = News.objects.latest('id').id




