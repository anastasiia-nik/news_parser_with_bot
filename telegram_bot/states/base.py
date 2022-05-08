from telebot import types


class BaseState:
    text = ''

    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    def display(self):
        self.bot.send_message(self.chat_id, self.text, reply_markup=self.get_keyboard())

    def get_keyboard(self):
        return None

    def send_warning(self, text):
        self.bot.send_message(self.chat_id, text)

    def process_call_back(self, message: types.CallbackQuery) -> 'BaseState':
        return self.__class__

    def process_text_message(self, message: types.Message) -> 'BaseState':
        return self.__class__