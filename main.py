import datetime
import telebot
from telebot import apihelper
from telebot.types import Message
import logging

from credentials import BOT_TOKEN, PROXY
from commands.commands_dict import init_light_command, init_sudo_command
from db.models import init_db
from utils import admin_list
from scheduler import scheduler_init

# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)
# logger_peewee = logging.getLogger('peewee')
# logger_peewee.addHandler(logging.StreamHandler())
# logger_peewee.setLevel(logging.DEBUG)

bot = telebot.TeleBot(BOT_TOKEN)
apihelper.proxy = {'https': 'socks5://{}'.format(PROXY)}

print('@@@ => INITIALIZE DATABASE <= @@@')
init_db()
print('@@@ => INITIALIZE SCHEDULER <= @@@')
scheduler_init()
print('@@@ => INITIALIZE BOT', bot.get_me(), '<= @@@')


# INITIALIZE AVAILABLE COMMANDS
light_commands = init_light_command('flood', 'share', 'tut', 'web', 'wq')
sudo_commands = init_sudo_command('ban', 'unban', 'sudo', 'warn')


@bot.message_handler(regexp='^![a-z]')
def handle_message(message: Message):
    """
    Main command handler. All members can use light commands. Admins and sudo can use admins commands.
    Users can`t notify admins with this commands.
    :param message: Telegram API message
    """
    user_id, command = message.from_user.id, message.text.split()[0].lower()
    bot.delete_message(message.chat.id, message.message_id)
    if message.reply_to_message and not message.reply_to_message.from_user.is_bot:
        reply_to = message.reply_to_message
        if reply_to and not reply_to.from_user.is_bot and reply_to.from_user.id not in admin_list(message.chat.id, bot):
            if command:
                try:
                    light_commands[command](message, bot)
                except (AttributeError, KeyError, TypeError):
                    try:
                        if user_id in admin_list(message.chat.id, bot):
                            sudo_commands[command](message, bot)
                    except (AttributeError, KeyError, TypeError):
                        pass


@bot.message_handler(content_types=['new_chat_members'])
def handler_new_member(message: Message):
    """
    New member mute chat group for 5 minutes.
    Working if add user from group or user join by self.
    NOTE! mute_till.strftime('%s') not working on windows platform! Using timestamp() * 1000
    :param message: Telegram API message
    """
    mute_till = datetime.datetime.now() + datetime.timedelta(minutes=5)
    bot.restrict_chat_member(
        message.chat.id,
        message.new_chat_member.id,
        until_date=mute_till.timestamp() * 1000,
        can_send_media_messages=False,
        can_add_web_page_previews=False,
        can_send_other_messages=False,
        can_send_messages=False
    )


bot.polling()
