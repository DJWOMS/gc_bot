import telebot
from telebot.types import Message
from typing import Callable
from utils import get_or_create_user


def warn_process(message: Message, result: Callable, bot: telebot):
    user, created = get_or_create_user(message.reply_to_message)
    if user:
        bot.reply_to(message.reply_to_message, text=result(
            message.from_user.username,
            user,
            message
        ), parse_mode='markdown')