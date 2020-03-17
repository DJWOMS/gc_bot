"""Helper utility for project"""

import datetime
import telebot
from telebot.types import Message
from db.models import User

def get_or_create_user(message: Message) -> User:
    """
    Check user in db. Return if exists or create new instance.
    Creating user from telegram api result message with keys username, first_name and so on
    :param message: telegram api result message
    :return User: User instance from db
    """
    return User.get_or_create(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )


def prepare_user_data(user: User) -> str:
    """
    Get user data. Non None fields for text response.
    :param user: Telegram user after saving in db
    :return str: not None user fields
    """
    attrs = ['first_name', 'last_name']
    banned_user = [getattr(user, attr) for attr in dir(user) if attr in attrs]
    b_user = ' '.join([i for i in banned_user if i is not None])
    return b_user


def to_unix_time(message: Message) -> tuple:
    """
    This shitless function need to be overriden.
    Parse message and get ban time in unix timestamp.
    :param message: Telegram API Message
    :return tuple: Text. Unix timestamp else None
    """
    msg = message.text.split()
    if len(msg) > 1:
        days, hours, minutes = 0, 0, 0
        vals = ['d', 'h', 'm']
        if len(msg[-1]) > 3 and not msg[-1].endswith(tuple(vals)):
            text = msg[-1]
        else:
            text = ''
        till = None
        for data in msg:
            try:
                if data.endswith(vals[0]):
                    days = int(data[:-1])
                if data.endswith(vals[1]):
                    hours = int(data[:-1])
                if data.endswith(vals[2]):
                    minutes = int(data[:-1])
                till = datetime.datetime.now() + datetime.timedelta(days=days, hours=hours, minutes=minutes)
            except ValueError:
                pass
        return till, text


def admin_list(chat_id: int, bot: telebot) -> list:
    """
    Get all admins in group
    :param chat_id: Telegram chat id integer number
    :param bot: Telebot instance
    :return list: Id`s list of all admins in groups
    """
    admins = bot.get_chat_administrators(chat_id)
    return [admin.user.id for admin in admins]

