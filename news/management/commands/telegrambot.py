from django.core.management.base import BaseCommand, CommandError
from dotenv import load_dotenv


from news.models import Category

import os
import telebot

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Hi!")


@bot.message_handler(func=lambda message: True)
def echo_all(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Hi!")


class Command(BaseCommand):

    def handle(self, *args, **options):
        # app.start_pooling()
        # print(os.getenv('TELEGRAM_TOKEN'))
        bot.infinity_polling()