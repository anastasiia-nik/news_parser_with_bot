import logging
import traceback

from django.db import IntegrityError

from demo.celery import app
from news.models import Comment
from news.parsers.apply_pars import apply_pars

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
    logger.info(msg)
