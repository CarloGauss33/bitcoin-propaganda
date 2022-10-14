import random
import cryptocompare
import datetime
import pytz

from configuration import config
from process_memes import MemeManager

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.ext.jobqueue import JobQueue


MESSAGE_POOL = [
    "Bitcoin is the future!",
    "Bitcoin is Freedom!",
    "Don't be fooled by the banks!"
]


class BitcoinTelegramManager:
    def __init__(self):
        self.updater = Updater(token=config.telegram_token)
        self.dispatcher = self.updater.dispatcher
        self.bot = self.updater.bot
        self.job_queue = self.updater.job_queue
        self.meme_service = MemeManager(config.memes_path, config.meme_state_path)
        self.__init_handlers()
        self.start_jobs()

    def __init_handlers(self):
        self.dispatcher.add_handler(CommandHandler('start', self.__start))
        self.dispatcher.add_handler(CommandHandler('meme', self.__meme))
        self.dispatcher.add_handler(CommandHandler('reminder', self.__reminder))
        self.dispatcher.add_handler(CommandHandler('set_broadcast', self.__broadcast_daily_reminder, pass_job_queue=True))

    def start_jobs(self):
        timezone = pytz.timezone("America/Santiago")
        t = datetime.time(12, 0, 0, 0, timezone)
        self.job_queue.run_daily(self.broadcast_message, time=t, days=tuple(range(7)))

    def __start(self, update: Update, context: CallbackContext):
        update.message.reply_text("Don't trust, verify!")

    def __meme(self, update: Update, context: CallbackContext):
        meme = self.meme_service.get_random_meme()
        update.message.reply_photo(photo=open(meme.path, 'rb'))

    def __reminder(self, update: Update, context: CallbackContext):
        message = self.message_build()
        update.message.reply_text(message)

    def message_build(self):
        price = cryptocompare.get_price('BTC', 'USD')
        message = "Daily reminder: Buy Bitcoin!\n\n"
        message += f"{MESSAGE_POOL[random.randint(0, len(MESSAGE_POOL) - 1)]}\n"
        message += f"Bitcoin is at ${price['BTC']['USD']} USD\n\n"
        message += "Don't trust, verify!\n"
        message += "Buda Referal -> https://buda.com/registro?rf=UX5WGU1R3"
        return message

    def broadcast_message(self, message: str, with_meme: bool = False):
        message = self.message_build()

        for chat_id in config.chat_ids:
            self.bot.send_message(chat_id=chat_id, text=message)
            if with_meme:
                meme = self.meme_service.get_random_meme()
                self.bot.send_photo(chat_id=chat_id, photo=open(meme.path, 'rb'))

    def __broadcast_daily_reminder(self, update: Update, context: CallbackContext):
        if config.chat_id_in_list(update.message.chat_id):
            update.message.reply_text("Removing reminder")
            config.remove_chat_id(update.message.chat_id)
            return

        config.add_chat_id(update.message.chat_id)
        update.message.reply_text("Reminder added")



bitcoin_bot_telegram = BitcoinTelegramManager()
bitcoin_bot_telegram.updater.start_polling()