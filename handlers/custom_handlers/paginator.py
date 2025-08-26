from typing import Dict

from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram_bot_pagination import InlineKeyboardPaginator

from loader import bot


user_data_hotels = {}


def transform_data(hotels: Dict, history: bool) -> Dict:
    data = {}
    for key, val in hotels.items():
        if history:
            text = (f"Название гостиницы - {val['name']}\n\n"
                    f"Ссылка на бронирование - {val['url']}\n\n"
                    f"Описание - {val['description']}\n\n"
                    f"Стоимость проживания за ночь - {round(val['price_per_night'], 2)} долларов США\n\n"
                    f"Координаты - {val['latitude']}, {val['longitude']}\n\n"
                    f"Чтобы посмотреть фоторгафии, нажмите кнопку 'Фото отеля'")
        else:
            text = (f"Название гостиницы - {val['name']}\n\n"
                    f"Ссылка на бронирование - {val['url']}\n\n"
                    f"Описание - {val['description']}\n\n"
                    f"Стоимость проживания за {val['number_of_nights']} ноч. - {round(val['gross_price'], 2)} долларов США\n\n"
                    f"Проживание с {val['arrival_date']} по {val['departure_date']}\n\n"
                    f"Координаты - {val['latitude']}, {val['longitude']}\n\n"
                    f"Чтобы посмотреть фоторгафии, нажмите кнопку 'Фото отеля'")
        data[key] = {}
        data[key]['text'] = text
        data[key]['photos'] = val['photos']

    return data


def call_paginator(hotels: Dict, message: Message, history: bool) -> None:
    hotels = transform_data(hotels, history=history)

    page = 1

    paginator = InlineKeyboardPaginator(
        len(hotels),
        current_page=page,
        data_pattern='page#{page}'
    )

    paginator.add_before(InlineKeyboardButton(f'Фото отеля {page}', callback_data='фото#{}'.format(page)))

    bot.send_message(
        message.chat.id,
        hotels[0]['text'],
        reply_markup=paginator.markup,
    )

    # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    #     data['hotels'] = hotels
    user_data_hotels[message.chat.id] = hotels


@bot.callback_query_handler(func=lambda call: call.data.startswith('page#'))
def callback_query(call):
    page = int(call.data.split('#')[1])

    # with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
    #     hotels = data['hotels']
    hotels = user_data_hotels.get(call.message.chat.id, {})

    paginator = InlineKeyboardPaginator(
        len(hotels),
        current_page=page,
        data_pattern='page#{page}'
    )

    paginator.add_before(InlineKeyboardButton(f'Фото отеля {page}', callback_data='фото#{}'.format(page)))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=hotels[page - 1]['text'],
        reply_markup=paginator.markup,
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('фото#'))
def send_photos(call):
    page = int(call.data.split('#')[1])
    chat_id = call.message.chat.id

    # with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
    #     photos = data['hotels'][page - 1]['photos']
    photos = user_data_hotels.get(chat_id, {}).get(page - 1, {}).get('photos', [])

    media_group = [InputMediaPhoto(photo) for photo in photos]

    bot.send_media_group(chat_id=chat_id,media=media_group)