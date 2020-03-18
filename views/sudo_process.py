import telebot
from telebot.types import Message
from typing import Callable

from db.models import User
from utils import get_or_create_user, prepare_user_data


def sudo_process(message: Message, bot: telebot):
    """
    Add or remove user from sudoers
    :param message: Telegram API Message
    :param result: Selected function from function dictionary.
    :param bot: Telebot instance
    """
    msg = message.text.split()
    if len(msg) > 1:
        user, created = get_or_create_user(message.reply_to_message)
        is_sudo = user.is_sudo
        user = prepare_user_data(user)
        if user or created:
            if 'add' in msg:
                if not is_sudo:
                    User.update(is_sudo=True).where(User.telegram_id == message.reply_to_message.from_user.id).execute()
                    msg = f'`{user} добавлен в группу sudoers`'
                    bot.send_message(message.from_user.id, text=msg, parse_mode='markdown')
                else:
                    msg = f'`{user} уже состоит в группе sudoers`'
                    bot.send_message(message.from_user.id, text=msg, parse_mode='markdown')
            elif 'del' in msg:
                if is_sudo:
                    User.update(is_sudo=False).where(User.telegram_id == message.reply_to_message.from_user.id).execute()
                    msg = f'`{user} удален из группы sudoers`'
                    bot.send_message(message.from_user.id, text=msg, parse_mode='markdown')
                else:
                    msg = f'`{user} не состоит в группе sudoers`'
                    bot.send_message(message.from_user.id, text=msg, parse_mode='markdown')
        else:
            bot.send_message(message.from_user.id, text='Ошибка операции sudo')