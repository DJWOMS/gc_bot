from datetime import datetime

from telebot.types import Message
from db.models import User, BlackList
from utils import prepare_user_data, to_unix_time


def ban_user(username: Message, user: User, reason: Message) -> str:
    """
    First checking if user is already banned (in db). If not then adding banned user in db.
    :param username: int: telegram user who send the command to ban
    :param user: User instance: user which need to ban
    :param reason: telebot Message: message to reply in telegram with reason to ban
    :return str: message to telegram chat about ban a specific user
    """
    dt, text = to_unix_time(reason)
    BlackList.create(user=user, datetime_add=datetime.today().strftime('%Y-%m-%d %H:%M:%S'), till_date=dt)
    banned_user = prepare_user_data(user)
    dt = dt.split('.')[:-1]
    if text and banned_user:
        return f'*{username} забанил пользователя {banned_user} До:{dt}\nПричина:*\n`{text}`'
    else:
        return f'*{username} забанил пользователя {banned_user} До: {dt}*'
