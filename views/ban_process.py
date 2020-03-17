import telebot
from telebot.types import Message
from typing import Callable

from utils import to_unix_time, get_or_create_user


def ban_process(message: Message, result: Callable, bot: telebot) -> Message:
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
        user, created = get_or_create_user(message.reply_to_message)
        if created:
            if msg[1] == 'kick':
                # kick user from chat aka ban forever
                response = bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            else:
                bot.send_photo(
                    chat_id=message.chat.id,
                    photo='AgACAgIAAxkDAAIBt15iuBjifOydpm759urePec6VHJgAALirDEbV48YS6MzQ4NoFW4IRSbBDgAEAQADAgADbQADhKoDAAEYBA',
                    caption=result(
                        message.from_user.username,
                        user,
                        message
                    ),
                    reply_to_message_id=message.reply_to_message,
                    parse_mode='markdown',
                )
                # ban user for specific time
                dt, _ = to_unix_time(message)
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
