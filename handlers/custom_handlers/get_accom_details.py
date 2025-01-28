from telebot.types import Message, ReplyKeyboardRemove
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date, timedelta
import time

from api.core import url, headers
from api.utils.site_api_handler import make_response
from keyboards.reply.destination import request_destination
from loader import bot, user_data
from states.accom_details import AccommodationDetailsStates


@bot.message_handler(commands=["get_accom_details"])
def get_accom_details(message: Message) -> None:
    bot.set_state(message.from_user.id, AccommodationDetailsStates.city, message.chat.id)
    bot.send_message(message.from_user.id, "Введите латиницей локацию для поиска отелей.")


@bot.message_handler(state=AccommodationDetailsStates.city)
def get_city(message: Message) -> None:

    querystring = {"query": message.text}
    dest_data = make_response(url, headers=headers, params=querystring, endpoint="searchDestination")

    if not isinstance(dest_data, dict):
        bot.send_message(message.from_user.id, "Что-то пошло не так. Попробуйте ввести другую локацию.")
        return

    bot.set_state(message.from_user.id, AccommodationDetailsStates.verif_location, message.chat.id)
    bot.send_message(message.from_user.id,
                     "Спасибо. Записал. Теперь уточните локацию, нажав на соответствующую кнопку.",
                     reply_markup=request_destination(dest_data))

    # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    #     data['flag'] = False
    #     data['city'] = message.text
    #     data['callback_data_dict'] = {}
    #     for val in dest_data["data"]:
    #         data['callback_data_dict'][val["label"]] = f"{val["dest_id"]}|{val["search_type"]}"
    user_data[message.chat.id] = {}
    user_data[message.chat.id]['flag'] = False
    user_data[message.chat.id]['city'] = message.text
    user_data[message.chat.id]['callback_data_dict'] = {}
    for val in dest_data["data"]:
        user_data[message.chat.id]['callback_data_dict'][val["label"]] = f"{val["dest_id"]}|{val["search_type"]}"


@bot.message_handler(state=AccommodationDetailsStates.verif_location)
def get_verif_location(message: Message) -> None:
    bot.set_state(message.from_user.id, AccommodationDetailsStates.arrival_date, message.chat.id)
    bot.send_message(message.from_user.id, "Спасибо. Записал. Теперь выберите дату заезда.", reply_markup=ReplyKeyboardRemove())
    calendar, step = DetailedTelegramCalendar(
        min_date=date.today(),
        max_date=date.today() + timedelta(days=365)
    ).build()
    bot.send_message(message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)

    # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    #     data['verif_location'] = message.text
    #     data['dest_id'], data['search_type'] = data['callback_data_dict'][data['verif_location']].split("|")
    #     del data['callback_data_dict']
    user_data[message.chat.id]['verif_location'] = message.text
    user_data[message.chat.id]['dest_id'], user_data[message.chat.id]['search_type'] \
        = user_data[message.chat.id]['callback_data_dict'][user_data[message.chat.id]['verif_location']].split("|")
    del user_data[message.chat.id]['callback_data_dict']


@bot.message_handler(state=AccommodationDetailsStates.price_min)
def get_price_min(message: Message) -> None:
    if message.text.isdigit():
        bot.set_state(message.from_user.id, AccommodationDetailsStates.price_max, message.chat.id)
        bot.send_message(message.from_user.id, "Спасибо. Записал. Теперь введите максимальную стоимость проживания в сутки в долларах США.")

        # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        user_data[message.chat.id]['price_min'] = message.text

    else:
        bot.send_message(message.from_user.id, "Стоимость может быть только числом. Введите еще раз.")


@bot.message_handler(state=AccommodationDetailsStates.price_max)
def get_price_max(message: Message) -> None:
    if message.text.isdigit():
        # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        user_data[message.chat.id]['price_max'] = message.text
        user_data[message.chat.id]['flag'] = True

        text = (f"Спасибо за предоставленную информацию. Ваши данные:\n\n"
                f"\tрасположение гостиницы - {user_data[message.chat.id]['verif_location']};\n\n"
                f"\tбронирование гостиницы с {user_data[message.chat.id]['arrival_date']} по {user_data[message.chat.id]['departure_date']};\n\n"
                f"\tобщее количество ночей - {user_data[message.chat.id]['number_of_nights']};\n\n"
                f"\tваш бюджет (за ночь) {user_data[message.chat.id]['price_min']} - {user_data[message.chat.id]['price_max']} долларов США\n\n"
                f"Далее можете выбирать гостиницы. Введите команду /help, чтобы получить справку")
        bot.send_message(message.from_user.id, text)
        bot.delete_state(message.from_user.id, message.chat.id)

    else:
        bot.send_message(message.from_user.id, "Стоимость может быть только числом. Введите еще раз.")