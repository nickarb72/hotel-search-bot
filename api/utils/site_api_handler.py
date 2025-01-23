from typing import Dict
import requests
from telebot.types import Message

from api.core import headers, url
from loader import bot


def make_response(url: str, headers: Dict, params: Dict, endpoint: str, timeout=10, success=200) -> Dict:
    url = "{}{}".format(url, endpoint)

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=timeout
    )

    status_code = response.status_code

    if status_code == success:
        return response.json()

    return status_code


def get_hotels(message: Message, sort_by: str) -> Dict:
    hotels = {}
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        print(data['flag'])
    number_of_nights = 3  # data['number_of_nights']
    querystring = {
        "dest_id":"-2607370", #data['dest_id']
        "search_type":"city", #data['search_type']
        "arrival_date":"2025-03-01", #data['arrival_date']
        "departure_date":"2025-03-04", #data['departure_date']
        "price_min":"300", #data['price_min'] * data['number_of_nights']
        "price_max":"600", #data['price_max'] * data['number_of_nights']
        "sort_by": sort_by, #"price", "popularity", "distance"
        "categories_filter":"price",
        "languagecode":"ru",
        "currency_code":"USD"
    }
    response = make_response(url, headers=headers, params=querystring, endpoint="searchHotels")

    if response['message'] == 'Success':
        for i in range(5):
            hotels[i] = {}
            hotels[i]['name'] = response['data']['hotels'][i]['property']['name']
            hotels[i]['id'] = response['data']['hotels'][i]['property']['id']
            hotels[i]['arrival_date'] = response['data']['hotels'][i]['property']['checkinDate']
            hotels[i]['departure_date'] = response['data']['hotels'][i]['property']['checkoutDate']
            hotels[i]['latitude'] = response['data']['hotels'][i]['property']['latitude']
            hotels[i]['longitude'] = response['data']['hotels'][i]['property']['longitude']
            hotels[i]['gross_price'] = response['data']['hotels'][i]['property']['priceBreakdown']['grossPrice']['value']
            hotels[i]['price_per_night'] = hotels[i]['gross_price'] / number_of_nights
            hotels[i]['number_of_nights'] = number_of_nights

            querystring = {
                "hotel_id": hotels[i]['id'],
                "arrival_date": hotels[i]['arrival_date'],
                "departure_date": hotels[i]['departure_date'],
                "languagecode": "ru",
                "currency_code": "USD"
            }
            url_response = make_response(url, headers=headers, params=querystring, endpoint="getHotelDetails")
            hotels[i]['url'] = url_response['data']['url']

            querystring = {
                "hotel_id": hotels[i]['id'],
                "languagecode": "ru",
            }
            description_response = make_response(url, headers=headers, params=querystring, endpoint="getDescriptionAndInfo")
            hotels[i]['description'] = description_response['data'][0]['description']

            querystring = {
                "hotel_id": hotels[i]['id']
            }
            photo_response = make_response(url, headers=headers, params=querystring, endpoint="getHotelPhotos")
            hotels[i]['photos'] = []
            for i_photo in range(5):
                hotels[i]['photos'].append(photo_response['data'][i_photo]['url'])

    return hotels