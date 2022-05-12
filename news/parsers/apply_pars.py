import logging

import news.parsers.news_pars2 as pu
from django.core.management.base import BaseCommand, CommandError
import news.models as nm

logger = logging.getLogger()

def apply_pars():
    upravda = pu.Upravda()
    upravda.parse_all()
    if upravda.all_news:
        add_tags(upravda)
        add_news(upravda)
    # print(f'collected {len(upravda.all_news)} news')
    logger.info(f'collected {len(upravda.all_news)} news')
    return len(upravda.all_news)



def add_authors(parser: pu.Upravda):
    nm.Author.objects.bulk_create([nm.Author(name=news.news_author) for news in parser.all_news],
                                  ignore_conflicts=True)


def add_tags(parser: pu.Upravda):
    tags = set()
    for news in parser.all_news:
        tags.update(set(news.news_tags))
    nm.Tags.objects.bulk_create([nm.Tags(tag=tag) for tag in tags], ignore_conflicts=True)


def add_news(parser: pu.Upravda):
    for news in parser.all_news:
        author_current, _ = nm.Author.objects.get_or_create(name=news.news_author, )
        category_current, _ = nm.Category.objects.get_or_create(name='upravda')
        news_tags = nm.Tags.objects.filter(tag__in=news.news_tags)
        news, _ = nm.News.objects.get_or_create(
            title=news.news_title, defaults={'date': news.news_data, 'text': news.news_text,
                                             'author': author_current, 'category': category_current,
                                             'image': news.news_photo, 'link': news.news_link})
        news.tags.clear()
        news.tags.add(*news_tags)
