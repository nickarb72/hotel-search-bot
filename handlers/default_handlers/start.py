from telebot.types import Message

from loader import bot

user_states = {}


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    if message.from_user.id not in user_states:
        user_states[message.from_user.id] = True
        bot.send_message(message.chat.id, 'Добро пожаловать в сервис по поиску отелей!'
                                          ' Увидеть полный список функций можно по команде /help')
    else:
        bot.send_message(message.chat.id, f'Рад вас снова видеть, {message.from_user.first_name}!'
                                          f' Увидеть полный список функций можно по команде /help')
