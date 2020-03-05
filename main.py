import telebot

from credentials import BOT_TOKEN
from commands import commands_dict


bot = telebot.TeleBot(BOT_TOKEN)
print(bot.get_me())


@bot.message_handler(func=lambda mess: '!web' == mess.text, content_types=['text'])
def handle_message(message):
    user_id, command = message.from_user.id, message.text.lower()
    bot.delete_message(message.chat_id, message.message_id)
    result = commands_dict.light_commands[command]
    if result:
        try:
            bot.reply_to(message.reply_to_message, text=result(), parse_mode='markdown', disable_web_page_preview=True)
        except AttributeError:
            pass


bot.polling()
