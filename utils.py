from db.models import User
from telebot.types import Message


def build_user(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    return User(
        id=user_id,
        username=username,
        first_name=user_first_name,
        last_name=user_last_name
    )
