import emoji
from loguru import logger

from src.bot import bot
from src.constants import keyboards, keys, states
from src.db import col
from src.utils.filters import IsAdmin
# from src.utils.io import read_json_file, write_file, write_json_file


class Bot:
    """
    a class for constructing a random anonymous connecter Telegram bot
    """

    def __init__(self, telebot) -> None:
        self.bot = telebot

        # add custom filters
        self.bot.add_custom_filter(IsAdmin())

        # register handlers
        self.handlers()

        # register database
        self.db = col

        # run bot
        logger.info('Bot is running...')
        self.bot.infinity_polling()

    def handlers(self):
        """
        Handling the chat messages in different conditions
        """
        @bot.message_handler(commands=['start'])
        def send_welcome(message):
            bot.reply_to(message, emoji.emojize(f"Hey <strong> {message.chat.first_name} </strong> :vulcan_salute: \
				 \n\nHope you enjoy the Bot! \n\n:backhand_index_pointing_right: send /help to continue "))

            # updating the database with the user data
            self.db.update_one({'chat.id': message.chat.id},
                               {'$set': message.json},
                               upsert=True)

            # Initializing the state of the user
            self.update_state(message.chat.id, states.main)

        @bot.message_handler(commands=['help'])
        def send_clue(message):
            bot.reply_to(message, emoji.emojize(f":busts_in_silhouette: This is a bot for connecting you to a random stranger with out revealing any identity from both sides!  \
					\n\nPress Connect buttun and wait until someone shows up :hourglass_not_done:"), reply_markup=keyboards.main)

        @bot.message_handler(regexp=emoji.emojize(keys.connect))
        def connect_stranger(message):
            """
            Handles if the connect button has been pressed and search for someone else to connect users
            """
            self.send_message(
                message.chat.id,
                'Bot is searching to find someone ...',
                reply_markup=keyboards.discard)

            # Updating the state of the current user to searching for someone to chat
            self.update_state(message.chat.id, states.random_connect)

            # Finding a stranger who is in the same state of searching
            other_usr = self.db.find_one({
                'state': states.random_connect,
                'chat.id': {'$ne': message.chat.id}}
            )

            if not other_usr:
                return

                # Updating the state of the current user and the recipient to from searching to connected
            self.update_state(message.chat.id, states.connected)

            self.send_message(
                message.chat.id,
                emoji.emojize(f":speech_balloon: Msg from system: \
				\n\nWe connected you to someone :flexed_biceps: \
					\n\nSay hello to your anonymous recipient."))

            self.update_state(other_usr['chat']['id'], states.connected)

            self.send_message(
                other_usr['chat']['id'],
                emoji.emojize(f":speech_balloon: Msg from system: \
				\n\nWe connected you to someone :flexed_biceps: \
					\n\n Say hello to your anonymous recipient."))

            # store connected users in database
            self.db.update_one(
                {'chat.id': message.chat.id},
                {'$set': {'connected_to': other_usr['chat']['id']}}
            )

            self.db.update_one(
                {'chat.id': other_usr['chat']['id']},
                {'$set': {'connected_to': message.chat.id}}
            )

        @bot.message_handler(regexp=emoji.emojize(keys.exit))
        def double_check(message):
            """
            Handles if the exit button has been pressed
            """
            self.send_message(
                message.chat.id,
                emoji.emojize(':speech_balloon: Msg from system: \
				\n\nAre you sure you want to end the chat? :thinking_face: '),
                reply_markup=keyboards.options)

        @bot.message_handler(regexp=emoji.emojize(keys.yes))
        def disconnect(message):
            """
            Handles if the yes button has been pressed
            """
            self.send_message(
                message.chat.id,
                emoji.emojize(':speech_balloon: Msg from system: \
				\n\nYou terminated this chat! \
					\n\n:backhand_index_pointing_right: What do you want me to do for you? '),
                reply_markup=keyboards.main)

            # update the state of the both users from connected to main
            self.update_state(message.chat.id, states.main)

            recipient_id = self.db.find_one(
                {'chat.id': message.chat.id}
            )['connected_to']

            if not recipient_id:
                return

            self.update_state(recipient_id, states.main)

            self.send_message(
                recipient_id,
                emoji.emojize(
                    f':speech_balloon: Msg from system: \
					\n\n {message.chat.first_name} just left the chat! \
					\n\n:backhand_index_pointing_right: What do you want me to do for you? '),
                reply_markup=keyboards.main)

            # remove connected users
            self.db.update_one(
                {'chat.id': message.chat.id},
                {'$set': {'connected_to': None}}
            )

            self.db.update_one(
                {'chat.id': recipient_id},
                {'$set': {'connected_to': None}}
            )

        @bot.message_handler(regexp=emoji.emojize(keys.no))
        def continue_(message):
            """
            Handles if the no button has been pressed
            """
            self.send_message(
                message.chat.id, emoji.emojize(':speech_balloon: Msg from system: \
					\n\n :OK_button: You can continue the chat ...'),
                reply_markup=keyboards.discard)

        # Method for sending message to admin of a group
        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
            self.send_message(
                message.chat.id, '<strong>You are admin of this group!</strong>')

        # Function for sending message to the random recipient
        @self.bot.message_handler(func=lambda _: True)
        def echo(message):

            sender = self.db.find_one(
                {'chat.id': message.chat.id}
            )

            if not sender or (sender['connected_to'] is None):
                return

            self.send_message(
                sender['connected_to'], message.text
            )

    # personalized method for sending message to the client
    def send_message(self, chat_id, text, reply_markup=None, emojize=True):
        if emojize:
            text = emoji.emojize(text, use_aliases=True)

        self.bot.send_message(
            chat_id, text,
            reply_markup=reply_markup
        )

    # Function for updating users state
    def update_state(self, chat_id, state):
        """
        Update the state of the user
        """
        col.update_one(
            {'chat.id': chat_id},
            {'$set': {'state': state}}
        )


if __name__ == '__main__':
    bot = Bot(telebot=bot)
    bot.run()
