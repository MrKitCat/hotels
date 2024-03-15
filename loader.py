from telebot import TeleBot
from config_data import config
from telebot.storage import StateMemoryStorage

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
