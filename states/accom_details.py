from telebot.handler_backends import State, StatesGroup


class AccommodationDetailsStates(StatesGroup):
    city = State()
    verif_location = State()
    arrival_date = State()
    departure_date = State()
    price_min= State()
    price_max = State()