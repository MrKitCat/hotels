from loader import bot
from telebot.types import Message
from loguru import logger
import datetime

from states.user_state import UserState
import keyboards
from keyboards.calendar import Calendar
import utills


@logger.catch
@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def low_high_best_handler(message: Message) -> None:
    """
    Обработка команд /lowprice, /highprice, /bestdeal
    После чего спрашиваем пользователя какой искать город.
    """
    bot.set_state(message.chat.id, UserState.command)
    with bot.retrieve_data(message.chat.id) as data:
        data.clear()
        logger.info(f'Пользователь ввел команду: {message.text} User_id: {message.chat.id}')
        data['command'] = message.text
        data['sort'] = check_command(message.text)
        data['date_time'] = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        data['chat_id'] = message.chat.id
    bot.set_state(message.chat.id, UserState.input_city)
    bot.send_message(message.from_user.id, "Введите город в котором нужно найти отель: ")


@logger.catch
@bot.message_handler(state=UserState.input_city)
def input_city(message: Message) -> None:
    """
    Ввод города и отправка запроса на сервер.
    Возможные варианты городов передаются генератору клавиатуры.

    """
    with bot.retrieve_data(message.chat.id) as data:
        data['input_city'] = message.text
        logger.info('Пользователь ввел город: ' + message.text + f' User_id: {message.chat.id}')
        url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {"q": message.text, "locale": "ru_RU"}

        response_cities = utills.requests.request('GET', url, querystring)
        if response_cities.status_code == 200:
            logger.info('Сервер ответил: ' + str(response_cities.status_code) + f' User_id: {message.chat.id}')
            possible_cities = utills.processing_json.get_city(response_cities.text)
            keyboards.make_a_buttons.show_cities_buttons(message, possible_cities)
        else:
            bot.send_message(message.chat.id, f"Что-то пошло не так, код ошибки: {response_cities.status_code}")
            bot.send_message(message.chat.id, 'Нажмите команду еще раз. И введите другой город.')
            data.clear()


@logger.catch
@bot.message_handler(state=UserState.hotels_count)
def hotels_amount(message: Message) -> None:
    """
    Сколько отелей показать на странице. Проверка количества отелей (число или нет)

    """
    if message.text.isdigit():
        if 0 < int(message.text) <= 25:
            logger.info('Ввод и запись количества отелей: ' + message.text + f' User_id: {message.chat.id}')
            with bot.retrieve_data(message.chat.id) as data:
                data['quantity_hotels'] = message.text
            bot.set_state(message.chat.id, UserState.price_min)
            bot.send_message(message.chat.id, 'Введите минимальную стоимость отеля в долларах США:')
        else:
            bot.send_message(message.chat.id, 'Ошибка! Это должно быть число в диапазоне от 1 до 25! Повторите ввод!')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@logger.catch
@bot.message_handler(state=UserState.price_min)
def input_price_min(message: Message) -> None:
    """
    Ввод минимальной стоимости отеля и проверка чтобы это было число.

    """
    if message.text.isdigit():
        logger.info(f'Пользователь ввел минимальную стоимость за ночь: {message.text}. User_id: {message.chat.id}')
        with bot.retrieve_data(message.chat.id) as data:
            data['price_min'] = message.text
        bot.set_state(message.chat.id, UserState.price_max)
        bot.send_message(message.chat.id, 'Введите максимальную стоимость отеля:')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@logger.catch
@bot.message_handler(state=UserState.price_max)
def input_price_max(message: Message) -> None:
    """
    Ввод максимальной стоимости отеля и проверка чтобы это было число. Максимальное число не может
    быть меньше минимального.

    """
    if message.text.isdigit():
        logger.info(
            f'Пользователь ввел максимальную стоимость номера в отеле. Сравниваем цены с минимальной стоимостью: '
            f'{message.text}. User_id: {message.chat.id}')
        with bot.retrieve_data(message.chat.id) as data:
            if int(data['price_min']) < int(message.text):
                data['price_max'] = message.text
                keyboards.make_a_buttons.show_buttons_photo_need_yes_no(message)
            else:
                bot.send_message(message.chat.id, 'Максимальная цена должна быть меньше минимальной. Повторите ввод!')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@logger.catch
@bot.message_handler(state=UserState.photo_count)
def input_photo_count(message: Message) -> None:
    """
    Ввод количества фотографий и проверка на число и на соответствие заданному диапазону от 1 до 10

    """
    if message.text.isdigit():
        if 0 < int(message.text) <= 10:
            logger.info(f'Пользователь выбрал показ фотографий: {message.text}. User_id: {message.chat.id}')
            with bot.retrieve_data(message.chat.id) as data:
                data['photo_count'] = message.text
            my_calendar(message, 'заезда')
        else:
            bot.send_message(message.chat.id, 'Число фотографий должно быть в диапазоне от 1 до 10! Повторите ввод!')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@logger.catch
@bot.message_handler(state=UserState.location_from)
def input_location_from(message: Message) -> None:
    """
    Ввод максимального расстояния до центра

    """
    if message.text.isdigit():
        logger.info(f'Пользователь ввел максимальное расстояние до центра:  {message.text} User_id: {message.chat.id}')
        with bot.retrieve_data(message.chat.id) as data:
            data['landmark_in'] = message.text
        bot.set_state(message.chat.id, UserState.location_to)
        bot.send_message(message.chat.id, 'Введите максимальное расстояние от центра (в милях).')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@logger.catch
@bot.message_handler(state=UserState.location_to)
def input_location_to(message: Message) -> None:
    """
    Ввод минимального расстояния до центра

    """
    if message.text.isdigit():
        logger.info(f'Пользователь ввел минимальное расстояние до центра:  {message.text} User_id: {message.chat.id}')
        with bot.retrieve_data(message.chat.id) as data:
            data['landmark_out'] = message.text
            utills.show_data_find_hotels.print_data(message, data)
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


def check_command(command: str) -> str:
    """
    Проверка команды и назначение параметра сортировки

    """
    if command == '/bestdeal':
        return 'DISTANCE'
    elif command == '/lowprice' or command == '/highprice':
        return 'PRICE_LOW_TO_HIGH'


bot_calendar = Calendar()


def my_calendar(message: Message, word: str) -> None:
    """
    Запуск (календаря) для выбора дат заезда и выезда

    """
    logger.info(f'Вызов календаря {word}. User_id: {message.chat.id}')
    bot.send_message(message.chat.id, f'Выберите дату: {word}',
                     reply_markup=bot_calendar.create_calendar(), )
