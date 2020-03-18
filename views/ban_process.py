import datetime
import telebot
from telebot.types import Message

from db.models import BlackList
from utils import to_unix_time, get_or_create_user, prepare_user_data


def ban_process(message: Message, bot: telebot) -> Message:
    """
    get_user_or_create check user in db and return user
    Creating User instance. Kicking user from chat and send group message about it.
    NOTE! mute_till.strftime('%s') not working on windows platform! Using timestamp() * 1000
    :param message: Current message data with user sender, chat_id and so on
    :param result: Selected function from function dictionary.
    :param bot: Telebot instance
    :return Message: Telegram result api message
    """
    msg = message.text.split()
    if len(msg) > 1:
        dt, text = to_unix_time(message)
        user, created = get_or_create_user(message.reply_to_message)
        BlackList.create(user=user, datetime_add=datetime.datetime.today(), till_date=dt)
        banned_user = prepare_user_data(user)
        till_date = dt.strftime('%Y-%m-%d %H:%M:%S')
        if text:
            msg = f'*{user.username} заблокировал пользователя {banned_user} До:{till_date}\nПричина:*\n`{text}`'
        else:
            msg = f'*{user.username} заблокировал пользователя {banned_user} До: {till_date}*'
        if created:
            if msg[1] == 'kick':
                # kick user from chat aka ban forever
                response = bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            else:
                bot.send_photo(
                    chat_id=message.chat.id,
                    photo='AgACAgIAAxkDAAIBt15iuBjifOydpm759urePec6VHJgAALirDEbV48YS6MzQ4NoFW4IRSbBDgAEAQADAgADbQADhKoDAAEYBA',
                    caption=msg,
                    reply_to_message_id=message.reply_to_message,
                    parse_mode='markdown',
                )
                # ban user for specific time
                response = bot.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    until_date=dt.timestamp() * 1000,
                    can_send_media_messages=False,
                    can_add_web_page_previews=False,
                    can_send_other_messages=False,
                    can_send_messages=False
                )
        else:
            response = '`Пользователь уже забанен`'
            bot.reply_to(message.reply_to_message, text=response, parse_mode='markdown')
        return response
