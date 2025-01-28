from telebot.handler_backends import State, StatesGroup


class HistoryStates(StatesGroup):
    query_date = State()
