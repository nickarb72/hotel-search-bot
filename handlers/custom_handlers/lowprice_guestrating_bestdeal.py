from pprint import pprint
from typing import Dict

from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram_bot_pagination import InlineKeyboardPaginator

from api.utils.site_api_handler import get_hotels
from loader import bot


user_data = {}


def transform_data(hotels: Dict) -> Dict:
    data = {}
    for key, val in hotels.items():
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


@bot.message_handler(commands=["lowprice", "guest_rating", "bestdeal"])
def lowprice_guestrating_bestdeal(message: Message) -> None:
    sorts = {"/lowprice": "price",
             "/guest_rating": "popularity",
             "/bestdeal": "distance"}

    command = message.text.split()[0]

    hotels = get_hotels(message, sorts[command])

 #    hotels = {0: {'arrival_date': '2025-03-01',
 #     'departure_date': '2025-03-04',
 #     'description': 'В этом объекте нельзя устраивать девичники, мальчишники и '
 #                    'другие подобные вечеринки.',
 #     'gross_price': 300.218301009273,
 #     'id': 10138295,
 #     'latitude': 50.704952845867,
 #     'longitude': -3.070586630688,
 #     'name': 'Seaton, Devon, two bed apartment, just off the sea front.',
 #     'number_of_nights': 3,
 #     'photos': ['https://cf.bstatic.com/xdata/images/hotel/square1024/614337622.jpg?k=f05865b82f205b0e17860576330757273ba8ea47b8e99ee1adb066d727ef6c9d&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/614338134.jpg?k=47c3dcaa325d7273138920187e9986a1a7f9d2f5d86d948dd02bf5b9ccb3eeb7&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/614337870.jpg?k=a1a11d6df042f972349e03d296c6552d0533dd97de551f43c2b2f3931491466a&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/614338337.jpg?k=8622a5e28c910c8f87fa1c69c1854115c17650a48247800bd908543c8a007270&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/614338248.jpg?k=e32c701ac9bac0af2ed5e7befd19f115cf9e1a458de3e88e58cd02ae4229e01f&o='],
 #     'price_per_night': 100.07276700309099,
 #     'url': 'https://www.booking.com/hotel/gb/seaton-devon-two-bed-apartment-just-off-the-sea-front.html'},
 # 1: {'arrival_date': '2025-03-01',
 #     'departure_date': '2025-03-04',
 #     'description': 'Пожалуйста, заранее сообщите Old Picture House '
 #                    'предполагаемое время прибытия. Вы можете использовать '
 #                    'поле «Особые пожелания» при бронировании или связаться с '
 #                    'объектом размещения напрямую — контактные данные указаны '
 #                    'в вашем подтверждении бронирования.\n'
 #                    'В этом объекте нельзя устраивать девичники, мальчишники и '
 #                    'другие подобные вечеринки.\n'
 #                    'В этом объекте нельзя останавливаться на карантин по '
 #                    'коронавирусу (COVID-19).',
 #     'gross_price': 313.662747397733,
 #     'id': 3850773,
 #     'latitude': 50.704152,
 #     'longitude': -3.067546,
 #     'name': 'Old Picture House',
 #     'number_of_nights': 3,
 #     'photos': ['https://cf.bstatic.com/xdata/images/hotel/square1024/201452698.jpg?k=87b736bfa50306c9ba83580a908c0cbb3b772b527e2028d643215ada894f541a&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/201452696.jpg?k=25033a2df6291bdec2fee728be3cc22b4efad97f9ffa4194b60b59db5349c6e8&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/201452687.jpg?k=df577f9e84dd97926d36e7693f45f3dab8daeb95ab74d9bcaffe0d2011a021b4&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/215545397.jpg?k=39c0c1c51764f0fc9e540ad8e7a60d33bd9c38d5636735e0ceeeaa4fc211bd64&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/345436126.jpg?k=54d53ef54d279a0d395b28138eb08269ae709b74fd8017d7d5b0de9b851b35f7&o='],
 #     'price_per_night': 104.55424913257768,
 #     'url': 'https://www.booking.com/hotel/gb/old-picture-house-devon.html'},
 # 2: {'arrival_date': '2025-03-01',
 #     'departure_date': '2025-03-04',
 #     'description': 'В этом объекте нельзя устраивать девичники, мальчишники и '
 #                    'другие подобные вечеринки.',
 #     'gross_price': 314.991201386711,
 #     'id': 12957528,
 #     'latitude': 50.6956334,
 #     'longitude': -3.1857819,
 #     'name': '#1 Stoneleigh Cottage',
 #     'number_of_nights': 3,
 #     'photos': ['https://cf.bstatic.com/xdata/images/hotel/square1024/605640720.jpg?k=46982b509dadce5598b901b7ef1200a3b1440654e815dbd2a6d1f74f63041563&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/605640776.jpg?k=04fc1e56182fbb89db4d8e096f0c9241ad01417271133ffea40b4ac2c44edf8e&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/605640783.jpg?k=7f01190c5e9a945e467b7b057119f8f5d70e5865e7bc79adfe73cc5e125c16a8&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/605640791.jpg?k=5a1ecd2c4950e3504be14ce2469a0d12619438511d678aba003717403ab96a36&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/605640799.jpg?k=e0e29c804a660e5e5a4dba46a9a528768bdd0cd61d4a1cedcd74a6558e196fec&o='],
 #     'price_per_night': 104.99706712890367,
 #     'url': 'https://www.booking.com/hotel/gb/1-stoneleigh-cottage.html'},
 # 3: {'arrival_date': '2025-03-01',
 #     'departure_date': '2025-03-04',
 #     'description': 'Этот уютный отель с популярным пабом находится в 150 м от '
 #                    'моря, в центре главной улицы города Ситон.\n'
 #                    '\n'
 #                    'По утрам сервируется полный английский завтрак.\n'
 #                    '\n'
 #                    'В воскресенье во второй половине дня в пабе играет живая '
 #                    'музыка, а летом можно поужинать на открытом воздухе.\n'
 #                    '\n'
 #                    'Отель Eyre Court удобно расположен для прогулок по '
 #                    'побережью залива Лайм.',
 #     'gross_price': 319.45,
 #     'id': 236939,
 #     'latitude': 50.7047054968217,
 #     'longitude': -3.07121783494949,
 #     'name': 'The Eyre Court',
 #     'number_of_nights': 3,
 #     'photos': ['https://cf.bstatic.com/xdata/images/hotel/square1024/228351558.jpg?k=86b8c735a5a0d832bf190c172f571b20133705e378007773418c5e29536939e4&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/632852456.jpg?k=7ef83fbb21a8a7150a8f6c40c39665e5c0b02bc28cfac398c7a5445ea839731f&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/228351547.jpg?k=29dc79b1385592ce2a643948ae0ee16774ddf4a6dd74aadc3a4230386682fccd&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/632852493.jpg?k=187796f35876473edff3f8d4be6a3c23be93d82e8c31963b214730ea1d4f15e3&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/236767051.jpg?k=d9e1d99c27f424590aba888707c6b5b8dab66f31d16ab4ad92d0722eeca82afe&o='],
 #     'price_per_night': 106.48333333333333,
 #     'url': 'https://www.booking.com/hotel/gb/the-eyre-court.html'},
 # 4: {'arrival_date': '2025-03-01',
 #     'departure_date': '2025-03-04',
 #     'description': 'Turnstone — это апартаменты на первой линии города Ситон, '
 #                    'в 300 м от такой достопримечательности, как Пляж Ситон. '
 #                    'Среди удобств есть сад и бесплатный Wi-Fi. Гости '
 #                    'апартаментов могут отдохнуть на патио.\n'
 #                    '\n'
 #                    'В распоряжении гостей этих апартаментов спальня (1), '
 #                    'гостиная, полностью оборудованная кухня с холодильником и '
 #                    'чайником, а также ванная комната (1) с душем и феном. '
 #                    'Гостям этих апартаментов предоставляются полотенца и '
 #                    'постельное белье.\n'
 #                    '\n'
 #                    'В окрестностях можно заняться велосипедными прогулками.\n'
 #                    '\n'
 #                    'Turnstone располагается в 26 км и 32 км соответственно от '
 #                    'таких достопримечательностей, как Холм Голден-Кэп и '
 #                    'Стадион для регби «Санди-Парк». Международный аэропорт '
 #                    'Эксетер находится в 31 км.',
 #     'gross_price': 335.250124718636,
 #     'id': 10138398,
 #     'latitude': 50.7042294,
 #     'longitude': -3.0691261,
 #     'name': 'Turnstone',
 #     'number_of_nights': 3,
 #     'photos': ['https://cf.bstatic.com/xdata/images/hotel/square1024/463506057.jpg?k=8c8ee9d46162c7f3e45a0b714ffaec068802a48385c37052bafd1ef5ea5f11e1&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/554383652.jpg?k=403e9b90bc45fcb8c5696c934e875b5e57ab04472cc08eb665026d17f1b86ccc&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/568602390.jpg?k=7a71b09415e119c17bcca0d96148c54264a8c28bdcc418f3b2733edda78178f7&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/554383162.jpg?k=41e78eea598958324ef58255dd4fd09b3c6e262379606d3b59a8861858c0359d&o=',
 #                'https://cf.bstatic.com/xdata/images/hotel/square1024/554383081.jpg?k=aecf9609c510bf2c5745e4e3151124deb301d470eb4ec641712625af7c521b42&o='],
 #     'price_per_night': 111.75004157287867,
 #     'url': 'https://www.booking.com/hotel/gb/a-quaint-bolt-hole-in-a-central-location.html'}}

    hotels = transform_data(hotels)

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
    user_data[message.chat.id] = hotels


@bot.callback_query_handler(func=lambda call: call.data.startswith('page#'))
def callback_query(call):
    page = int(call.data.split('#')[1])

    # with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
    #     hotels = data['hotels']
    hotels = user_data.get(call.message.chat.id, {})

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

    # with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
    #     photos = data['hotels'][page - 1]['photos']
    photos = user_data.get(call.message.chat.id, {}).get(page - 1, {}).get('photos', [])

    media_group = [InputMediaPhoto(photo) for photo in photos]

    bot.send_media_group(
        chat_id=call.message.chat.id,
        media=media_group
    )

