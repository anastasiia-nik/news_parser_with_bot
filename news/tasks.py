import logging
import traceback
from datetime import datetime

from django.db import IntegrityError
from django.http import HttpRequest
from django.urls import reverse, get_script_prefix

from demo.celery import app
from news.models import Comment, Tags, Subscriber, News, LastSendedNews
from news.parsers.apply_pars import apply_pars
from telegram_bot import main

logger = logging.getLogger()


@app.task()
def math(a, b):
    return a + b


@app.task()
def store_comment(author, text, news_id):
    logger.info(f"{author=}, {text=}")
    try:
        Comment.objects.create(
            author=author,
            text=text, news_id_id=news_id
        )
    except IntegrityError:
        logger.error(traceback.format_exc())
        logger.error("Error saving")


@app.task()
def store_statistic():
    logger.info("all ok")


@app.task()
def update_news_base():
    msg = apply_pars()
    logger.info(f'collected {msg} news')
    last_news_sent = LastSendedNews.objects.get(id=1)
    # last_news_date = News.objects.get(id=last_news_id).date

    # if msg > 0:
    subscribers = Subscriber.objects.all()
    # last_news = News.objects.filter(date__gt=last_news_date).values('link')
    last_news = News.objects.filter(id__gt=last_news_sent.news_id).values('slug')
    last_news_sent.news_id = News.objects.latest('id').id
    last_news_sent.save()

    for link in last_news:
        for subscriber in subscribers:
            # send_news_to_subscriber.delay(subscriber.chat_id,
            # #                               HttpRequest.build_absolute_uri(reverse('article_name', args=[link['slug']])))
            # send_news_to_subscriber.delay(subscriber.chat_id, 'https://%s%s' % (Site.objects.get_current().domain) + '/article_' + link['slug'])
            send_news_to_subscriber.delay(subscriber.chat_id, f'https://django.py-beetroot.ml/article_{link["slug"]}')


@app.task()
def send_news_to_subscriber(chat_id, msg):
    main.bot.send_message(chat_id, msg)
