import telebot
from telebot.types import Message


def web_process(message: Message, bot: telebot) -> Message:
    """Links to searching engine"""
    msg = """
    Похоже необходимо воспользоваться поиском:\n\n*+* https://google.com/\n*+* https://duckduckgo.com/
    """
    return bot.reply_to(message.reply_to_message, text=msg, parse_mode='markdown',
                        disable_web_page_preview=True)
