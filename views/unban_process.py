import telebot
from telebot.types import Message
from typing import Callable


def unban_process(message: Message, result: Callable, bot: telebot):
    """
    Delete user from user and blacklist tables.
    :param message: Telegram API Message
    :param result: Selected function form commands dict
    :param bot: Telebot instance
    """
    bot.reply_to(message.reply_to_message, text=result(
        message,
    ), parse_mode='markdown')
