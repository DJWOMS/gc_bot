from telebot.types import Message

from db.models import User, Warns
from utils import prepare_user_data


def warn_user(username: Message, user: User, reason: Message) -> str:
    warns_count = Warns.select().where(user_id=User.id)
    # warning_user = prepare_user_data(user)
    # warnings_count = user.warn
    # reason = ' '.join(reason.text.split(' ')[1:])
    # if warnings_count < 2:
    #     warnings_count += 1
    #     User.update(warn=warnings_count).where(User.telegram_id == user.telegram_id).execute()
    #     if reason and warning_user:
    #         return f'*{username} предупредил пользователя {warning_user}\nПричина:*\n`{reason}`'
    #     else:
    #         return f'*{username} предупредил пользователя {warning_user}*'
    # else:
    #     warnings_count += 1
    #     User.update(warn=warnings_count).where(User.telegram_id == user.telegram_id).execute()
    #     if reason:
    #         return f'*{username} предупредил пользователя {warning_user}\nПричина:*\n`{reason}`'
    #     else:
    #         return f'*{username} предупредил пользователя {warning_user}*'
