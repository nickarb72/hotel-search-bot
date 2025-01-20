from telebot.types import Message
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date, timedelta

from api.core import url, headers
from api.utils.site_api_handler import make_response
from keyboards.reply.destination import request_destination
from loader import bot
from states.accom_details import AccommodationDetailsStates


@bot.message_handler(commands=["get_accom_details"])
def get_accom_details(message: Message) -> None:
    bot.set_state(message.from_user.id, AccommodationDetailsStates.city, message.chat.id)
    bot.send_message(message.from_user.id, "Введите латиницей локацию для поиска отелей.")


@bot.message_handler(state=AccommodationDetailsStates.city)
def get_city(message: Message) -> None:

    querystring = {"query": message.text}
    dest_data = make_response(url, headers=headers, params=querystring, endpoint="searchDestination")

    bot.set_state(message.from_user.id, AccommodationDetailsStates.verif_location, message.chat.id)
    bot.send_message(message.from_user.id,
                     "Спасибо. Записал. Теперь уточните локацию, нажав на соответствующую кнопку.",
                     reply_markup=request_destination(dest_data))

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text
        data['callback_data_dict'] = {}
        for val in dest_data["data"]:
            data['callback_data_dict'][val["label"]] = f"{val["dest_id"]}|{val["search_type"]}"


@bot.message_handler(state=AccommodationDetailsStates.verif_location)
def get_verif_location(message: Message) -> None:
    bot.set_state(message.from_user.id, AccommodationDetailsStates.arrival_date, message.chat.id)
    bot.send_message(message.from_user.id, "Спасибо. Записал. Теперь выберите дату заезда.")
    calendar, step = DetailedTelegramCalendar(
        min_date=date.today(),
        max_date=date.today() + timedelta(days=365)
    ).build()
    bot.send_message(message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['verif_location'] = message.text
        data['dest_id'], data['search_type'] = data['callback_data_dict'][data['verif_location']].split("|")
        del data['callback_data_dict']


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
            with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
                today = date.today()
                arrival_date = result

                if arrival_date < today:
                    bot.send_message(c.message.chat.id, "Дата заезда не может быть раньше сегодняшней даты. Пожалуйста, выберите другую дату.")
                    return

                data['arrival_date'] = result
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
            with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
                arrival_date = data.get('arrival_date')
                departure_date = result

                if departure_date < arrival_date:
                    bot.send_message(c.message.chat.id, "Дата выезда не может быть раньше даты заезда. Пожалуйста, выберите другую дату.")
                    return

                data['departure_date'] = result
                data['number_of_nights'] = (data['departure_date'] - data['arrival_date']).days
                bot.set_state(c.from_user.id, AccommodationDetailsStates.price_min, c.message.chat.id)
                bot.edit_message_text(f"Вы выбрали дату выезда: {result}. Теперь введите минимальную стоимость проживания в сутки в долларах США.",
                                      c.message.chat.id,
                                      c.message.message_id)


@bot.message_handler(state=AccommodationDetailsStates.price_min)
def get_price_min(message: Message) -> None:
    if message.text.isdigit():
        bot.set_state(message.from_user.id, AccommodationDetailsStates.price_max, message.chat.id)
        bot.send_message(message.from_user.id, "Спасибо. Записал. Теперь введите максимальную стоимость проживания в сутки в долларах США.")

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['price_min'] = message.text

    else:
        bot.send_message(message.from_user.id, "Стоимость может быть только числом. Введите еще раз.")


@bot.message_handler(state=AccommodationDetailsStates.price_max)
def get_price_max(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['price_max'] = message.text

            text = (f"Спасибо за предоставленную информацию. Ваши данные:\n"
                    f"\tрасположение гостиницы - {data['verif_location']};\n"
                    f"\tбронирование гостиницы с {data['arrival_date']} по {data['departure_date']};\n"
                    f"\tобщее количество ночей - {data['number_of_nights']};\n"
                    f"\tваш бюджет (за ночь) {data['price_min']} - {data['price_max']} долларов США\n\n"
                    f"Далее можете выбирать гостиницы. Введите команду /help, чтобы получить справку")
            bot.send_message(message.from_user.id, text)
            bot.delete_state(message.from_user.id, message.chat.id)

    else:
        bot.send_message(message.from_user.id, "Стоимость может быть только числом. Введите еще раз.")