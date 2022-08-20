from telebot import types
import emoji


def create_keyboards(*keys, row_width=2, resize_keyboard=True):
    """
    create a keyboard from a list of keys
    """
    markup = types.ReplyKeyboardMarkup(
        row_width=row_width,
        resize_keyboard=resize_keyboard
    )
    keys = map(emoji.emojize, keys)
    buttons = map(types.KeyboardButton, keys)
    markup.add(*buttons)

    return markup