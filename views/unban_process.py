import telebot
from telebot.types import Message
from typing import Callable

from db.models import User


def unban_process(message: Message, bot: telebot) -> Message:
    """
    Delete user from user and blacklist tables.
    :param message: Telegram API Message
    :param bot: Telebot instance
    :return response message from Telegram API server
    """
    user = User.delete().where(User.telegram_id == message.reply_to_message.from_user.id).execute()
    if user:
        msg = '`Пользователь разблокирован`'
    else:
        msg = '*Пользователь не заблокирован*'

    return bot.reply_to(message.reply_to_message, text=msg, parse_mode='markdown')
