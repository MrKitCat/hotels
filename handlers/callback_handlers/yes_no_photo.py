from loader import bot
from loguru import logger
from telebot.types import CallbackQuery
from states.user_state import UserState
from handlers.custom_handlers.input_data import my_calendar

@logger.catch
@bot.callback_query_handler(func=lambda call: call.data.isalpha())
def yes_no_photo(call: CallbackQuery) -> None:
    """Обработка запроса вывода фотографий отеля. Да/Нет"""
    if call.data == 'yes':
        logger.info(f'Пользователь хочет посмотреть фотографии отелей. User_id: {call.message.chat.id}')
        with bot.retrieve_data(call.message.chat.id) as data:
            data['photo_need'] = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.chat.id, UserState.photo_count)
        bot.send_message(call.message.chat.id, 'Сколько вывести фотографий? (От 1 до 10!)')
    elif call.data == 'no':
        logger.info(f'Фотографии выводится не будут. User_id: {call.message.chat.id} ')
        with bot.retrieve_data(call.message.chat.id) as data:
            data['photo_need'] = call.data
            data['photo_count'] = '0'
        bot.delete_message(call.message.chat.id, call.message.message_id)
        my_calendar(call.message, 'заезда')