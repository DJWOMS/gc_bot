import telebot
from telebot.types import Message
from typing import Callable
from utils import get_or_create_user


def sudo_process(message: Message, result: Callable, bot: telebot):
    """
    Add or remove user from sudoers
    :param message: Telegram API Message
    :param result: Selected function from function dictionary.
    :param bot: Telebot instance
    """
    user, created = get_or_create_user(message.reply_to_message)
    if user:
        bot.send_message(message.from_user.id, text=result(message, user), parse_mode='markdown')