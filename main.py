import telebot
from telebot.types import Message

from credentials import BOT_TOKEN
from commands import commands_dict
from utils import build_user
from db.sqlite_utils import (
    init_db, add_user,
    count_sudo_users, count_banned_users,
    count_warn_users, update_user
)

bot = telebot.TeleBot(BOT_TOKEN)
init_db()
print(bot.get_me())


@bot.message_handler(regexp='^![a-z]')
def handle_message(message: Message):
    user_id, command = message.from_user.id, message.text.split(' ')[0].lower()
    bot.delete_message(message.chat.id, message.message_id)
    if message.reply_to_message and not message.reply_to_message.from_user.is_bot:
        try:
            result = commands_dict.light_commands[command]
            if result:
                bot.reply_to(message.reply_to_message, text=result(), parse_mode='markdown',
                             disable_web_page_preview=True)
        except (AttributeError, KeyError):
            if user_id == 169603089:
                try:
                    result = commands_dict.sudo_commands[command]
                    if result and result.__name__.split('_')[0] == 'ban':
                        user = build_user(message.reply_to_message)
                        bot.reply_to(message.reply_to_message, text=result(user), parse_mode='markdown')
                    elif result and result.__name__.split('_')[0] == 'warn':
                        bot.reply_to(message.reply_to_message, text=result(), parse_mode='markdown')
                    elif result and result.__name__.split('_')[0] == 'unban':
                        bot.reply_to(message.reply_to_message, text=result(), parse_mode='markdown')
                    elif result and result.__name__.split('_')[0] == command[1:]:
                        bot.reply_to(message.reply_to_message, text=result(), parse_mode='markdown')
                except (AttributeError, KeyError, TypeError):
                    pass


bot.polling()
