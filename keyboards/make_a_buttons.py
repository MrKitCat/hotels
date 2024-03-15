from loader import bot
from telebot import types
from loguru import logger
from telebot.types import Message, Dict


def show_buttons_photo_need_yes_no(message: Message) -> None:
    """
    Inline-клавиатура с предложением вывода фотографий.

    """
    logger.info(f'Выбор вывода фотографий отелей или нет. User_id: {message.chat.id}')
    keyboard_yes_no = types.InlineKeyboardMarkup()
    keyboard_yes_no.add(types.InlineKeyboardButton(text='ДА', callback_data='yes'))
    keyboard_yes_no.add(types.InlineKeyboardButton(text='НЕТ', callback_data='no'))
    bot.send_message(message.chat.id, "Вывести фотографии отелей?", reply_markup=keyboard_yes_no)


def show_cities_buttons(message: Message, possible_cities: Dict) -> None:
    """
    Inline-клавиатура с выбором города из списка.

    """
    logger.info(f'Вывод списка городов. User_id: {message.chat.id}')
    keyboards_cities = types.InlineKeyboardMarkup()
    for key, value in possible_cities.items():
        keyboards_cities.add(types.InlineKeyboardButton(text=value["regionNames"], callback_data=value["gaiaId"]))
    bot.send_message(message.from_user.id, "Выберите город", reply_markup=keyboards_cities)