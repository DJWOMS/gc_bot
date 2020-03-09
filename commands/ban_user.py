from telebot.types import Message
from db.models import User, BlackList


def prepare_user_data(user: User) -> str:
    """
    Get user data. Non None fields for text response.
    :param: user User: Telegram user after saving in db
    :return str: not None user fields
    """
    attrs = ['first_name', 'last_name']
    banned_user = [getattr(user, attr) for attr in dir(user) if attr in attrs]
    b_user = ' '.join([i for i in banned_user if i is not None])
    return b_user


def ban_user(username: Message, user: User, reason: Message) -> str:
    """
    First checking if user is already banned (in db). If not then adding banned user in db.
    :param username: int: telegram user who send the command to ban
    :param user: User instance: user which need to ban
    :param reason: telebot Message: message to reply in telegram with reason to ban
    :return str: message to telegram chat about ban a specific user
    """
    bl = BlackList.create(user=user)
    print(bl)
    reason = ' '.join(reason.text.split(' ')[1:])
    if reason and prepare_user_data:
        return f'*{username} забанил пользователя {prepare_user_data}\nПричина:*\n`{reason}`'
    else:
        return f'*{username} забанил пользователя {user.username}*'
