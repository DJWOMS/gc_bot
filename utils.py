"""Helper utility for project"""

from db.models import User
from telebot.types import Message


def get_or_create_user(message: Message) -> User:
    """
    Check user in db. Return if exists or create new instance.
    Creating user from telegram api result message with keys username, first_name and so on
    :param message: telebot Message: telegram api result message
    :return: User instance
    """
    return User.get_or_create(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
