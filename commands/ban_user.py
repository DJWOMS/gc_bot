from telebot.types import Message
from db.models import User


def ban_user(username: Message, user: User, reason: Message) -> str:
    """
    First checking if user is already banned (in db). If not then adding banned user in db.
    :param username: int: telegram user who send the command to ban
    :param user: User instance: user which need to ban
    :param reason: telebot Message: message to reply in telegram with reason to ban
    :return str: message to telegram chat about ban a specific user
    """
    attrs = ['first_name', 'last_name']
    banned_user = [getattr(user, attr) for attr in dir(user) if attr in attrs]
    b_user = ' '.join([i for i in banned_user if i is not None])
    user, created = User.get_or_create(**user)

    reason = ' '.join(reason.text.split(' ')[1:])
    if reason and b_user:
        return f'*{username} забанил пользователя {b_user}\nПричина:*\n`{reason}`'
    else:
        return f'*{username} забанил пользователя {user.username}*'
