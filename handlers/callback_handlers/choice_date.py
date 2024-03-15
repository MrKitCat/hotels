from loader import bot
from loguru import logger
import datetime
from telebot.types import CallbackQuery

from states.user_state import UserState
from keyboards.calendar import CallbackData, Calendar, check_date
import handlers.custom_handlers.input_data
import utills

calendar = Calendar()
calendar_callback = CallbackData("calendar", "action", "year", "month", "day")

@logger.catch
@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_callback.prefix))
def input_date(call: CallbackQuery) -> None:
    """
    Выбор даты заезда. Сравниваем с текущим днем. Дата заезда должна быть либо сегодня, либо в
    любой следующий день. А дата выезда не может быть меньше, либо равна, дате заезда.
    """
    name, action, year, month, day = call.data.split(calendar_callback.sep)
    calendar.calendar_query_handler(
        bot=bot,
        call=call,
        name=name,
        action=action,
        year=year,
        month=month,
        day=day
    )

    if action == 'DAY':
        logger.info(f'Пользователь {call.from_user.id} указал дату. User_id: {call.message.chat.id}')
        month = check_date(month)
        day = check_date(day)
        select_date = year + month + day

        now_year, now_month, now_day = datetime.datetime.now().strftime('%Y.%m.%d').split('.')
        now = now_year + now_month + now_day

        bot.set_state(call.message.chat.id, UserState.check_in_out_dates)
        with bot.retrieve_data(call.message.chat.id) as check_in_date:
            if 'checkInDate' in check_in_date:
                checking = int(check_in_date['checkInDate']['year'] + check_in_date['checkInDate']['month'] +
                               check_in_date['checkInDate']['day'])
                if int(select_date) > checking:
                    logger.info(f'Запись даты заезда пользователя. User_id: {call.message.chat.id}')
                    check_in_date['checkOutDate'] = {'day': day, 'month': month, 'year': year}
                    check_in_date['landmark_in'] = 0
                    check_in_date['landmark_out'] = 0
                    if check_in_date['sort'] == 'DISTANCE':
                        bot.set_state(call.message.chat.id, UserState.location_from)
                        bot.send_message(call.message.chat.id, 'Введите минимальное расстояние до центра.')
                    else:
                        utills.show_data_find_hotels.print_data(call.message, check_in_date)
                else:
                    bot.send_message(call.message.chat.id, 'Дата выезда должна быть больше даты заезда! '
                                                           'Повторите выбор даты!')
                    handlers.custom_handlers.input_data.my_calendar(call.message, 'выезда')
            else:
                logger.info(f'Запись даты заезда пользователя. User_id: {call.message.chat.id}')
                check_in_date['checkInDate'] = {'day': day, 'month': month, 'year': year}
                handlers.custom_handlers.input_data.my_calendar(call.message, 'выезда')
