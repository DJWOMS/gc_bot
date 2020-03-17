from telebot.types import Message
from db.models import User
from utils import prepare_user_data


def unban_user(message: Message) -> str:
    """
    Unban user process
    :param user: User: db User
    :param message: Telegram API message
    :return: str: String as text for chat message
    """
    user = User.delete().where(User.telegram_id == message.reply_to_message.from_user.id).execute()
    if user:
        return '`Пользователь разблокирован`'
    else:
        return '*Пользователь не заблокирован*'

