import telebot
from telebot.types import Message


def test_process(message: Message, bot: telebot) -> Message:
    """Complete the question with details.
    """
    msg = """
    Тест бота)))
    """
    return bot.reply_to(message.reply_to_message, text=msg, parse_mode='markdown',
                        disable_web_page_preview=True)
