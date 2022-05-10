from django.core.management import BaseCommand
from telegram_bot.main import bot


class Command(BaseCommand):

    def handle(self, *args, **options):
        # app.start_pooling()
        # print(os.getenv('TELEGRAM_TOKEN'))
        bot.infinity_polling()
