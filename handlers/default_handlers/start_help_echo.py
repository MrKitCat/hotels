from telebot.types import Message
import user_database
from loader import bot
from loguru import logger

from config_data.config import DEFAULT_COMMANDS

@logger.catch
@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
    user_database.creat_user_db.add_user(message)

@logger.catch
@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, '\n'.join(text))


@logger.catch
@bot.message_handler(func=lambda message: True)
def bot_echo(message: Message) -> None:
    if message.text == 'привет':
        bot.reply_to(message, f'Реагируем на слово "привет", И вам {message.from_user.full_name} - привет!')
    else:
        bot.reply_to(message, "Эхо без состояния или фильтра.\nСообщение:"
                              f"{message.text}")