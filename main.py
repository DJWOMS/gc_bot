from typing import Callable
import telebot
from telebot.types import Message
import logging

from credentials import BOT_TOKEN
from commands import commands_dict
from db.models import init_db, User, Sudo, BlackList
from utils import get_or_create_user
from config import MEDIA_ROOT

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(BOT_TOKEN)
init_db()
print(bot.get_me())


def ban_process(message: Message, result: Callable) -> Message:
    """
    get_user_or_create check user in db and return user
    Creating User instance. Kicking user from chat and send group message about it.
    :param: message: telebot Message: current message data with user sender, chat_id and so on
    :param: result: function: selected function from function dictionary.
    :return: Message: telegram result api message
    """
    user, created = get_or_create_user(message.reply_to_message)
    print(user, created)
    if created:
        # kick user from chat aka ban
        # response = bot.kick_chat_member(message.chat.id, message.reply_to_message)
        response = 'success'
        bot.send_photo(
            chat_id=message.chat.id,
            photo='AgACAgIAAxkDAAIBt15iuBjifOydpm759urePec6VHJgAALirDEbV48YS6MzQ4NoFW4IRSbBDgAEAQADAgADbQADhKoDAAEYBA',
            caption=result(
                message.from_user.username,
                user,
                message
            ),
            reply_to_message_id=message.reply_to_message,
            parse_mode='markdown')
    else:
        response = f'{message.reply_to_message} Уже забанен!'
    return response


def admin_list(chat_id: int) -> list:
    """
    Get all admins in group
    :param chat_id: int: telegram chat id
    :return: list: id`s list of all admins in groups
    """
    admins = bot.get_chat_administrators(chat_id)
    return [admin.user.id for admin in admins]


@bot.message_handler(regexp='^![a-z]')
def handle_message(message: Message):
    user_id, command = message.from_user.id, message.text.split(' ')[0].lower()
    bot.delete_message(message.chat.id, message.message_id)
    if message.reply_to_message and not message.reply_to_message.from_user.is_bot:
        try:
            result = commands_dict.light_commands[command]
            if result:
                bot.reply_to(message.reply_to_message, text=result(), parse_mode='markdown',
                             disable_web_page_preview=True)
        except (AttributeError, KeyError):
            if user_id in admin_list(message.chat.id):
                try:
                    result = commands_dict.sudo_commands[command]
                    if result and result.__name__.split('_')[0] == 'ban':
                        ban_process(message, result)
                    elif result and result.__name__.split('_')[0] == 'warn':
                        bot.reply_to(message.reply_to_message, text=result(), parse_mode='markdown')
                    elif result and result.__name__.split('_')[0] == 'unban':
                        bot.reply_to(message.reply_to_message, text=result(), parse_mode='markdown')
                    elif result and result.__name__.split('_')[0] == command[1:]:
                        bot.reply_to(message.reply_to_message, text=result(), parse_mode='markdown')
                except (AttributeError, KeyError, TypeError):
                    pass


bot.polling()
