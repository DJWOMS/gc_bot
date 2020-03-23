import telebot
from telebot.types import Message


def tut_process(message: Message, bot: telebot) -> Message:
    """
    Links to Django tutorials resources.
    :param message: Telegram API Message
    :param bot: Telebot instance
    :return response message from Telegram API server
    """
    msg = """
    Полезные обучающие материалы для начала:\n\n*+* https://docs.djangoproject.com/en/3.0/
*+* https://tutorial.djangogirls.org/ru/\n*+* https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/
*+* https://django.fun/docs/django/ru/3.0/
    """
    return bot.reply_to(message.reply_to_message, text=msg, parse_mode='markdown',
                        disable_web_page_preview=True)
