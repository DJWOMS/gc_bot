#### **Telegram BOT для администрирования группы**
- Бот обрабатывает два типа команд:
1. **light_commands**. Команды доступные обычным пользователям
2. **sudo_commands**. Команды доступные только _суперпользователям_. 

Каждой команде должен соответсвовать свой модуль в пакете **views**.

**Пример создания новой light команды для бота:**

1. ```main.py```

    ```light_commands = init_light_command(... 'test') # регистрируем новую команду 'test'```

2. В папке views создаем новый модуль ```test_process.py```. Название модуля может быть любым, но **обязательно
    разделяться нижним подчеркиванием _ и первое слово должно полностью соответствовать имени команды**.
    Хорошим тоном будет придерживаться следующему именованию '_command_process_.py'.
3. Внутри модуля ```test_process.py``` необходимо создать функцию с аналогичным именем.
    **Важно! Функция должна иметь то же имя, что и содержащий ее модуль**.
    ```test_process.py <- def test_process(): pass```.
 4. Функция принимает на вход два аргумета и возвращает один:
    ```def unban_process(message: Message, bot: telebot) -> Message: pass```.
    
    ```message``` - Сообщение от сервера Telegram API. Данное сообщение разбирается и из него
    достаются необходимые данные, такие как:
    
        - id пользователя
        - текст сообщения
        - id сообщения для ответа и так далее
        Подробнее: https://core.telegram.org/bots/api
        
    ```bot``` - экземпляр бота, для отправки сообщения в чат. Экземрляр создается один раз в ```main.py```
    и затем используется в функциях-представлениях.
    
    Функция возвращает ```Message``` - ответ от сервера Telegram.
    
 _Пример функции ```test```_
 
 ```python
import telebot
from telebot.types import Message


def test_process(message: Message, bot: telebot) -> Message:
    """Test function"""
    msg = """Hello world!"""
    return bot.reply_to(message.reply_to_message, text=msg, parse_mode='markdown',
                        disable_web_page_preview=True)
```
