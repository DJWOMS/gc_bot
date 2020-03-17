import datetime
import telebot
from telebot import apihelper
from telebot.types import Message
import logging

from credentials import BOT_TOKEN, PROXY
from commands.commands_dict import light_commands, sudo_commands
from db.models import init_db
from utils import admin_list
from scheduler import scheduler_init

# VIEWS
from views.ban_process import ban_process
from views.unban_process import unban_process
from views.sudo_process import sudo_process
from views.warn_process import warn_process

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

            try:
                result = light_commands[command]
                if result:
                    bot.reply_to(message.reply_to_message, text=result(), parse_mode='markdown',
                                 disable_web_page_preview=True)
            except (AttributeError, KeyError):
                if user_id in admin_list(message.chat.id, bot):
                    try:
                        result = sudo_commands[command]
                        if result and result.__name__.split('_')[0] == 'ban':
                            ban_process(message, result, bot)
                        elif result and result.__name__.split('_')[0] == 'warn':
                            warn_process(message, result, bot)
                        elif result and result.__name__.split('_')[0] == 'unban':
                            unban_process(message, result, bot)
                        elif result and result.__name__.split('_')[0] == 'sudo':
                            sudo_process(message, result, bot)
                        elif result and result.__name__.split('_')[0] == command[1:]:
                            bot.reply_to(message.reply_to_message, text=result(), parse_mode='markdown')
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
