import telebot
from telebot.types import Message


def share_process(message: Message, bot: telebot) -> Message:
    """Links to share code web stages"""
    msg = """
    Для того, чтобы поделиться `кодом` или `ошибкой`, необходимо воспользоваться онлайн сервисами, такими как:\n
*-* https://hastebin.com/\n*-* https://pastebin.com/\n*-* https://codeshare.io/
    """
    return bot.reply_to(message.reply_to_message, text=msg, parse_mode='markdown',
                        disable_web_page_preview=True)