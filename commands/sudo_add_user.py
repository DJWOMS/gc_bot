from telebot.types import Message
from db.models import User
from utils import prepare_user_data


def sudo_add_user(message: Message, user: User):
    process = message.text.split()[1:]
    is_sudo = user.is_sudo
    user = prepare_user_data(user)
    if 'add' in process:
        if not is_sudo:
            User.update(is_sudo=True).where(User.telegram_id == message.reply_to_message.from_user.id).execute()
            return f'`{user} добавлен в группу sudoers`'
        else:
            return f'`{user} уже состоит в группе sudoers`'
    elif 'del' in process:
        if is_sudo:
            User.update(is_sudo=False).where(User.telegram_id == message.reply_to_message.from_user.id).execute()
            return f'`{user} удален из группы sudoers`'
        else:
            return f'`{user} не состоит в группе sudoers`'
    else:
        return '`Ошибка операции sudo`'
