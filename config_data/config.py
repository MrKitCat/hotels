import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DB_NAME = os.getenv('DB_NAME')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Помощь по командам бота"),
    ('lowprice', "Вывод дешёвых отелей в городе"),
    ('highprice', "Вывод дорогих отелей в городе"),
    ('bestdeal', "Вывод отелей, наиболее подходящих по цене и расположению от центра"),
    ('history', "Вывод истории поиска отелей")
)
