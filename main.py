import datetime
from typing import Callable
import telebot
from telebot import apihelper
from telebot.types import Message
import logging

from credentials import BOT_TOKEN, PROXY
from commands import commands_dict
from commands import greet_new_member
from db.models import init_db, get_sudoers, User, BlackList
from utils import get_or_create_user, to_unix_time

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(BOT_TOKEN)
apihelper.proxy = {'https': 'socks5://{}'.format(PROXY)}

init_db()
sudoers = get_sudoers()

print('@@@ =>', bot.get_me(), '<= @@@')


def ban_process(message: Message, result: Callable) -> Message:
    """
    get_user_or_create check user in db and return user
    Creating User instance. Kicking user from chat and send group message about it.
    :param: message: telebot Message: current message data with user sender, chat_id and so on
    :param: result: function: selected function from function dictionary.
    :return: Message: telegram result api message
    """
    user, created = get_or_create_user(message.reply_to_message)
    if created:
        bot.send_photo(
            chat_id=message.chat.id,
            photo='AgACAgIAAxkDAAIBt15iuBjifOydpm759urePec6VHJgAALirDEbV48YS6MzQ4NoFW4IRSbBDgAEAQADAgADbQADhKoDAAEYBA',
            caption=result(
                message.from_user.username,
                user,
                message
            ),
            reply_to_message_id=message.reply_to_message,
            parse_mode='markdown')
        # kick user from chat aka ban
        dt, _ = to_unix_time(message)
        response = bot.restrict_chat_member(
            message.chat.id,
            message.reply_to_message.from_user.id,
            until_date=dt,
            can_send_media_messages=False,
            can_add_web_page_previews=False,
            can_send_other_messages=False,
            can_send_messages=False
        )
    else:
        response = '`Пользователь уже забанен`'
        bot.reply_to(message.reply_to_message, text=response, parse_mode='markdown')
    return response


def unban_process(message: Message):
    """Delete user from user and blacklist tables"""
    user = User.delete().where(User.telegram_id == message.reply_to_message.from_user.id).execute()
    BlackList.delete().where(BlackList.user_id == user).execute()


def warn_process(message: Message, result: Callable):
    print('here')
    user, created = get_or_create_user(message.reply_to_message)
    if user:
        bot.reply_to(message.reply_to_message, text=result(
            message.from_user.username,
            user,
            message
        ), parse_mode='markdown',)


def admin_list(chat_id: int) -> list:
    """
    Get all admins in group
    :param chat_id: int: telegram chat id
    :return: list: id`s list of all admins in groups
    """
    admins = bot.get_chat_administrators(chat_id)
    return [admin.user.id for admin in admins]


@bot.message_handler(regexp='^![a-z]')
def handle_message(message: Message):
    """Main command handler. All members can use light commands. Admins and sudo can use admins commands.
    Users can`t notify admins with this commands.
    """
    user_id, command = message.from_user.id, message.text.split(' ')[0].lower()
    bot.delete_message(message.chat.id, message.message_id)
    if message.reply_to_message and not message.reply_to_message.from_user.is_bot:
        try:
            result = commands_dict.light_commands[command]
            if result:
                bot.reply_to(message.reply_to_message, text=result(), parse_mode='markdown',
                             disable_web_page_preview=True)
        except (AttributeError, KeyError):
            if user_id in admin_list(message.chat.id):
                try:
                    result = commands_dict.sudo_commands[command]
                    if result and result.__name__.split('_')[0] == 'ban':
                        ban_process(message, result)
                    elif result and result.__name__.split('_')[0] == 'warn':
                        print('here0')
                        warn_process(message, result)
                    elif result and result.__name__.split('_')[0] == 'unban':
                        unban_process(message)
                    elif result and result.__name__.split('_')[0] == command[1:]:
                        bot.reply_to(message.reply_to_message, text=result(), parse_mode='markdown')
                except (AttributeError, KeyError, TypeError):
                    pass


@bot.message_handler(content_types=['new_chat_members'])
def handler_new_member(message: Message):
    """New member mute chat group for 5 minutes"""
    bot.send_message(message.chat.id, text=greet_new_member(), disable_notification=True)
    mute_till = datetime.datetime.now() + datetime.timedelta(minutes=5)
    print(message)
    bot.restrict_chat_member(
        message.chat.id,
        message.from_user.id,
        until_date=mute_till.strftime('%s'),
        can_send_media_messages=False,
        can_add_web_page_previews=False,
        can_send_other_messages=False,
        can_send_messages=False
    )


# @bot.message_handler(content_types=['text'])
# def test(message: Message):
#     print(message)


bot.polling()
