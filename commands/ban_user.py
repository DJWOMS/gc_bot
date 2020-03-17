from datetime import datetime
from telebot.types import Message
from db.models import User, BlackList
from utils import prepare_user_data, to_unix_time
from commands.unban_user import unban_user
from scheduler import init_scheduler
from db.models import printer


def ban_user(username: Message, user: User, message: Message) -> str:
    """
    First checking if user is already banned (in db). If not then adding banned user in db.
    :param username: Telegram user who send the command to ban. Integer value
    :param user: User which need to ban. User instance from db
    :param message: Telegram API message to reply in telegram with reason to ban
    :return str: Message to telegram chat about ban a specific user
    """
    dt, text = to_unix_time(message)
    BlackList.create(user=user, datetime_add=datetime.today(), till_date=dt)
    banned_user = prepare_user_data(user)
    till_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    scheduler = init_scheduler()
    scheduler.add_job(printer, 'date', run_date=till_date, args=[message])
    scheduler.start()
    print(scheduler.print_jobs())
    if text and banned_user:
        return f'*{username} заблокировал пользователя {banned_user} До:{till_date}\nПричина:*\n`{text}`'
    else:
        return f'*{username} заблокировал пользователя {banned_user} До: {till_date}*'
