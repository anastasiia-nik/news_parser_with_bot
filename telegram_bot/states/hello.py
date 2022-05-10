from telebot import types

from news.models import Subscriber, News
from telegram_bot.states.base import BaseState


class Hello(BaseState):
    text = "Доброго дня! Ви звернулися до чат-боту 'Новини'."

    def save_subscribe(self):
        subscriber = Subscriber.objects.get_or_create(chat_id=self.chat_id)
        last_news = News.objects.latest('date').link
        self.bot.send_message(self.chat_id, last_news)

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data and message.data == 'nextstate:SubscribedState':
            self.save_subscribe()
            return SubscribedState
        return Hello

    def get_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text='Пiдписатися на всi новини', callback_data='nextstate:SubscribedState'))
        return keyboard

class SubscribedState(BaseState):
    text = 'Ви успiшно пiдписалися на усi новини'

    def get_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text='Вiдписатися вiд новин', callback_data='nextstate:Hello'))
        return keyboard

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data and message.data == 'nextstate:Hello':
            self.unsubscribe()
            return Hello
        return SubscribedState

    def unsubscribe(self):
        Subscriber.objects.get(chat_id=self.chat_id).delete()


class ActionState(BaseState):
    text = 'Ви успiшно пiдписалися на усi новини'

    def process_text_message(self, message: types.Message) -> 'BaseState':
        # if message.text in ('1', '2', '3'):
        #     return ActionAppliedState
        # self.send_warning('Натисніть 1, 2 або 3!')
        return ActionState


class ActionAppliedState(BaseState):
    text = "Вибачте, всі оператори зайняті!"

    def get_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Додому', callback_data='nextstate:Hello'))
        return keyboard

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        if message.data and message.data == 'nextstate:Hello':
            return Hello
        return ActionAppliedState
