import telebot
from telebot.types import Message


def wq_process(message: Message, bot: telebot) -> Message:
    """Complete the question with details"""
    msg = """
    Для решения задачи недостаточно информации. Следует расширить вопрос, внеся в него детали проблемы
    """
    return bot.reply_to(message.reply_to_message, text=msg, parse_mode='markdown',
                        disable_web_page_preview=True)