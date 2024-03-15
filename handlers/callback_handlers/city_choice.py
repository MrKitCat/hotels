from loader import bot
from telebot.types import CallbackQuery
from loguru import logger

from states.user_state import UserState

@logger.catch
@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def destination_id_callback(call: CallbackQuery) -> None:
    """
    Запрос кол-ва отелей, в городе, который выбрал пользователь
    """
    logger.info(f'Пользователь выбрал город. User_id: {call.message.chat.id}')
    if call.data:
        bot.set_state(call.message.chat.id, UserState.destination_id)
        with bot.retrieve_data(call.message.chat.id) as data:
            data['destination_id'] = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.chat.id, UserState.hotels_count)
        bot.send_message(call.message.chat.id, 'Сколько отелей показать? (Не более 25!)')