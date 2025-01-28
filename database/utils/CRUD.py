from datetime import datetime
from typing import Dict

from database.common.models import History, Photos


def save_hotels_to_db(hotels: Dict, chat_id: int) -> None:
    for hotel_data in hotels.values():
        history = History.create(
            chat_id=chat_id,
            name=hotel_data['name'],
            url=hotel_data['url'],
            description=hotel_data['description'],
            price_per_night=hotel_data['price_per_night'],
            latitude=hotel_data['latitude'],
            longitude=hotel_data['longitude']
        )

        for photo_url in hotel_data['photos']:
            Photos.create(url=photo_url, hotel=history)


def get_hotels_by_date(date: datetime.date, chat_id: int) -> Dict:
    # query_date = datetime.strptime(date, '%Y-%m-%d').date()
    query = History.select().where((History.created_at == date) & (History.chat_id == chat_id))
    hotels = {}
    count = 0
    for history in query:
        hotel_data = {
            'created_at': history.created_at.strftime('%Y-%m-%d'),
            'name': history.name,
            'url': history.url,
            'description': history.description,
            'price_per_night': history.price_per_night,
            'latitude': history.latitude,
            'longitude': history.longitude,
            'photos': [photo.url for photo in history.photos]
        }
        hotels[count] = hotel_data
        count += 1
    return hotels