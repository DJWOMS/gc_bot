import telebot
from telebot.types import Message


def flood_process(message: Message, bot: telebot) -> Message:
    """
    Link to group for flooding wars.
    :param message: Telegram API Message
    :param bot: Telebot instance
    :return response message from Telegram API server
    """
    msg = """
    Группа для свободного общения, в которой вы можете обсуждать второстепенные вопросы и разводить холивары 
https://t.me/trueDjangoChannel

    """
    return bot.reply_to(message.reply_to_message, text=msg, parse_mode='markdown',
                        disable_web_page_preview=True)
