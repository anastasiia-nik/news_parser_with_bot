from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200)

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
        return f'{self.title}: {self.text}'

# Create your models here.
class Model:
    pass