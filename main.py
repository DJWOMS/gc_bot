import telebot
from telebot.types import Message

from credentials import BOT_TOKEN
from commands import commands_dict

bot = telebot.TeleBot(BOT_TOKEN)
print(bot.get_me())


@bot.message_handler(regexp='^![a-z]')
def handle_message(message: Message):
    user_id, command = message.from_user.id, message.text.lower()
    bot.delete_message(message.chat.id, message.message_id)
    try:
        result = commands_dict.light_commands[command]
        if result:
            bot.reply_to(message.reply_to_message, text=result(), parse_mode='markdown', disable_web_page_preview=True)
    except (AttributeError, KeyError):
        if user_id == 169603089:
            try:
                result = commands_dict.sudo_commands[command]
                if result and result == '!wall':
                    bot.reply_to(message.reply_to_message, text=result(), parse_mode='markdown',
                                 disable_web_page_preview=True)
                elif result:
                    pass
            except (AttributeError, KeyError):
                pass


bot.polling()
