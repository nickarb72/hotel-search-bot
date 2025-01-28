from telebot.types import Message

from api.utils.site_api_handler import get_hotels
from database.utils.CRUD import save_hotels_to_db
from loader import bot, user_data
from .paginator import call_paginator


@bot.message_handler(commands=["lowprice", "guest_rating", "bestdeal"])
def lowprice_guestrating_bestdeal(message: Message) -> None:
    flag = user_data.get(message.chat.id, {}).get('flag', False)
    if not flag:
        bot.send_message(message.from_user.id, "Сначала введите данные для поиска с помощью команды /get_accom_details")
        return

    sorts = {"/lowprice": "price",
             "/guest_rating": "popularity",
             "/bestdeal": "distance"}

    command = message.text.split()[0]

    hotels = get_hotels(message, sorts[command])

    if hotels == {}:
        bot.send_message(message.from_user.id,
                         "Что-то пошло не так. Попробуйте повторить запрос позже или изменить информацию для поиска с помощью команды /get_accom_details.")
        return

    save_hotels_to_db(hotels, message.chat.id)

    call_paginator(hotels, message, history=False)
