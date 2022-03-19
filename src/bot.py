import os

import telebot
from loguru import logger
from src.constants import keyboards
# from src.utils.io import read_json_file, write_file, write_json_file


class Bot:
    """
    basic ready to go template for a Telegram Bot
    """

    def __init__(self) -> None:
        self.bot = telebot.TeleBot(
            # replace your intended Bot Token into the belew string
            os.environ['BOT_TOKEN'], parse_mode=None)
        self.echo_all = self.bot.message_handler(
            func=lambda m: True)(self.echo_all)

    def run(self):
        logger.info('Bot is running ...')
        self.bot.infinity_polling()

    def echo_all(self, message):
        self.bot.send_message(message.chat.id, message.text,
                              reply_markup=keyboards.main)


if __name__ == '__main__':
    bot = Bot()
    bot.run()
