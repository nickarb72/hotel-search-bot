from typing import Dict
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_destination(data: Dict) -> ReplyKeyboardMarkup:
    buttons = []
    count = 0

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for val in data["data"]:
        buttons.append(KeyboardButton(text=val["label"]))
        keyboard.add(buttons[count])
        count += 1

    return keyboard


