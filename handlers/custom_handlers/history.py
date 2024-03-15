from loader import bot
from telebot.types import Message, InputMediaPhoto
from loguru import logger
import user_database
from states.user_state import UserState

@logger.catch
@bot.message_handler(commands=['history'])
def get_list_history(message: Message) -> None:
    """
    Показ истории поиска отелей

    """
    logger.info(f'Запуск команды history! User_id: {message.chat.id}')
    queries = user_database.read_user_db.read_query(message.chat.id)
    if queries:
        logger.info(f'Получены записи из таблицы query:\n {queries}. User_id: {message.chat.id}')
        for item in queries:
            bot.send_message(message.chat.id, f"({item[0]}). Дата и время: {item[1]}. Вы вводили город: {item[2]}")
        bot.set_state(message.chat.id, UserState.select_history)
        bot.send_message(message.from_user.id, "Введите номер интересующего вас варианта: ")
    else:
        bot.send_message(message.chat.id, 'История запросов пуста')

@logger.catch
@bot.message_handler(state=UserState.select_history)
def input_number(message: Message) -> None:
    """
    Запрос к базе данных и вывод результата в чат.

    """
    if message.text.isdigit():
        queries = user_database.read_user_db.read_query(message.chat.id)
        number_query = []
        show_photo = ''
        for item in queries:
            number_query.append(item[0])
            if int(message.text) == item[0] and item[3] == 'yes':
                show_photo = 'yes'

        if show_photo == 'no':
            bot.send_message(message.chat.id, 'Пользователь отказался от вывода фото')

        if int(message.text) in number_query:
            logger.info(f"Запрос к БД. User_id: {message.chat.id}")
            history_dict = user_database.read_user_db.get_history_response(message)
            with bot.retrieve_data(message.chat.id) as data:
                data.clear()
            if history_dict:
                logger.info(f'Вывод результата по запросу пользователя. User_id: {message.chat.id}')
                for hotel in history_dict.items():
                    medias = []
                    caption = f"Название отеля: {hotel[1]['name']}]\n Адрес отеля: {hotel[1]['address']}" \
                              f"\nСтоимость проживания в " \
                              f"сутки $: {hotel[1]['price']}\nРасстояние до центра: {hotel[1]['distance']}"
                    urls = hotel[1]['images']
                    if show_photo == 'yes':
                        for number, url in enumerate(urls):
                            if number == 0:
                                medias.append(InputMediaPhoto(media=url, caption=caption))
                            else:
                                medias.append(InputMediaPhoto(media=url))
                        bot.send_media_group(message.chat.id, medias)
                    else:
                        bot.send_message(message.chat.id, caption)
            else:
                bot.send_message(message.chat.id, "Ошибка! Попробуйте другие операции.")
                logger.info(f'Что-то пошло не так! User_id: {message.chat.id}')
        else:
            bot.send_message(message.chat.id, 'Ошибка! Ничего не найдено! Повторите ввод!')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')
    bot.set_state(message.chat.id, None)
