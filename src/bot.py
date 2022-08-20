import os

import telebot

# initialize bot
bot = telebot.TeleBot(
    # replace your intended Bot Token into the belew string
    os.environ['NASHENAS_BOT_TOKEN'], parse_mode='HTML')
