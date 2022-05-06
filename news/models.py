from datetime import datetime

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

    def __str__(self):
        return self.tag


class News(models.Model):
    title = models.CharField(max_length=500)
    date = models.DateTimeField(blank=True, null=True)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    image = models.ImageField(upload_to='news/images/', blank=True, null=True)


    def __str__(self):
        return f'{self.title}'

    @property
    def comment_counter(self):
        one_news = News.objects.get(id=self.id)
        return one_news.comments.filter(approved=True).count()


class Comment(models.Model):
    author = models.CharField(max_length=150, validators=[MinLengthValidator(2)])
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    news_id = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return 'Comment {} by {}'.format(self.text, self.author)


