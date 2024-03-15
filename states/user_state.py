from telebot.handler_backends import State, StatesGroup

class UserState(StatesGroup):
    """Класс состояния пользователя"""
    command = State()  # команда пользователя
    input_city = State()  # искомый город
    destination_id = State()  # id города
    hotels_count = State()  # количество отелей для поиска номеров
    photo_count = State()  # количество фотографий
    check_in_out_dates = State()  # ввод даты (заезда, выезда)
    price_min = State()  # минимальная стоимость отеля
    price_max = State()  # максимальная стоимость отеля
    location_from = State()  # начало диапазона расстояния от центра
    location_to = State()  # конец диапазона расстояния от центра
    select_history = State()  # выбор истории поиска