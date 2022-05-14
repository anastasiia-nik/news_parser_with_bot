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

@bot.message_handler(content_types=['photo'])
def photo(message):
    print(message)
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.delete_message(message.chat.id, message.message_id, 0)
    bot.send_photo(message.chat.id, open("cat.jpg", "rb"), "Лапкота!")

class Command(BaseCommand):

    def handle(self, *args, **options):
        # app.start_pooling()
        # print(os.getenv('TELEGRAM_TOKEN'))
        bot.infinity_polling()