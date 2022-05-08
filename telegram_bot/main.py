from django.core.management.base import BaseCommand, CommandError
from dotenv import load_dotenv


from news.models import Category

import os
import telebot

from telegram_bot.states.base import BaseState
from telegram_bot.states.hello import Hello

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
clients: dict = {}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    bot_new = Hello(bot, message.chat.id)
    bot_new.display()
    clients[message.chat.id] = Hello


@bot.callback_query_handler(func=lambda message: True)
def process_call_back(message):
    chat_id = message.from_user.id
    new_state_class = get_state(chat_id).process_call_back(message)
    clients[chat_id] = new_state_class
    display(chat_id)


@bot.message_handler(func=lambda message: True)
def echo_all(message: telebot.types.Message):
    chat_id = message.chat.id
    new_state_class = get_state(chat_id).process_text_message(message)
    clients[chat_id] = new_state_class
    display(chat_id)


def display(chat_id):
    state = get_state(chat_id)
    state.display()


def get_state(chat_id) -> BaseState:
    current_state = clients.get(chat_id, Hello)
    examples_of_class = current_state(bot, chat_id)
    return examples_of_class