from telebot.types import Message
from db.models import User


def ban_user(username: Message, user: User, reason: Message):
    attrs = ['username', 'first_name', 'last_name']
    banned_user = [getattr(user, attr) for attr in dir(user) if attr in attrs]
    b_user = ' '.join([i for i in banned_user if i is not None])
    if reason:
        reason = ' '.join(reason.text.split(' ')[1:])
        return f'{username} забанил пользавателя {b_user}\nПричина:\n{reason}'
    else:
        return f'{username} забанил пользователя {b_user}'
