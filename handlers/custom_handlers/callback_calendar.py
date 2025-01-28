from telebot.types import Message
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date, timedelta
import time

from database.utils.CRUD import get_hotels_by_date
from handlers.custom_handlers.paginator import call_paginator
from loader import bot, user_data
from states.accom_details import AccommodationDetailsStates


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)

    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        current_state = bot.get_state(c.from_user.id, c.message.chat.id)

        if current_state == "AccommodationDetailsStates:arrival_date":
            # with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
            today = date.today()
            arrival_date = result

            if arrival_date < today:
                message = bot.send_message(c.message.chat.id, "Дата заезда не может быть раньше сегодняшней даты. Пожалуйста, выберите другую дату.")
                time.sleep(5)
                bot.delete_message(c.message.chat.id, message.message_id)
                return

            user_data[c.message.chat.id]['arrival_date'] = result
            bot.set_state(c.from_user.id, AccommodationDetailsStates.departure_date, c.message.chat.id)
            bot.edit_message_text(f"Вы выбрали дату заезда: {result}. Теперь выберите дату выезда.",
                                  c.message.chat.id,
                                  c.message.message_id)

            calendar, step = DetailedTelegramCalendar(
                min_date=result,
                max_date=result + timedelta(days=365)
            ).build()
            bot.send_message(c.message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)

        elif current_state == "AccommodationDetailsStates:departure_date":
            # with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
            arrival_date = user_data[c.message.chat.id].get('arrival_date')
            departure_date = result

            if departure_date < arrival_date:
                message = bot.send_message(c.message.chat.id, "Дата выезда не может быть раньше даты заезда. Пожалуйста, выберите другую дату.")
                time.sleep(5)
                bot.delete_message(c.message.chat.id, message.message_id)
                return

            user_data[c.message.chat.id]['departure_date'] = result
            user_data[c.message.chat.id]['number_of_nights'] = (departure_date - arrival_date).days
            bot.set_state(c.from_user.id, AccommodationDetailsStates.price_min, c.message.chat.id)
            bot.edit_message_text(f"Вы выбрали дату выезда: {result}. Теперь введите минимальную стоимость проживания в сутки в долларах США.",
                                  c.message.chat.id,
                                  c.message.message_id)

        elif current_state == "HistoryStates:query_date":
            today = date.today()
            query_date = result

            if today < query_date:
                message = bot.send_message(c.message.chat.id, "Дата поиска не может быть позже сегодняшней даты. Пожалуйста, выберите другую дату.")
                time.sleep(5)
                bot.delete_message(c.message.chat.id, message.message_id)
                return

            bot.edit_message_text(f"Вы выбрали дату поиска: {result}.",
                                  c.message.chat.id,
                                  c.message.message_id)
            bot.delete_state(c.from_user.id, c.message.chat.id)

            hotels = get_hotels_by_date(result, c.message.chat.id)

            if hotels == {}:
                bot.send_message(c.message.chat.id,
                                 f"За {result} нет сохраненных запросов.")
                return

            call_paginator(hotels, c.message, history=True)