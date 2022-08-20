import telebot
from src.bot import bot


class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    # the class will check whether the user is admin or creater the group or not
    key = 'is_admin'

    @staticmethod
    def check(message: telebot.types.Message):
        return bot.get_chat_member(message.chat.id, message.from_user.id).status in ['administrator', 'creator']
