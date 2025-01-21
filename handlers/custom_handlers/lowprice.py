from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["lowprice"])
def lowprice(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        print(data['flag'])
        print(data['verif_location'])
    # if message.from_user.id not in user_states:
    #     user_states[message.from_user.id] = True
    #     bot.send_message(message.chat.id, 'Добро пожаловать в сервис по поиску отелей!'
    #                                       ' Увидеть полный список функций можно по команде /help')
    # else:
    #     bot.send_message(message.chat.id, f'Рад вас снова видеть, {message.from_user.first_name}!'
    #                                       f' Увидеть полный список функций можно по команде /help')
