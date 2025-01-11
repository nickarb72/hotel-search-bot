from telebot.types import Message

from loader import bot


@bot.message_handler(func=lambda message: "привет" in message.text.lower())
def bot_start(message: Message) -> None:
    bot.send_message(message.chat.id, 'Привет! Я бот по поиску отелей. Чтобы увидеть полный список моих функций, напишите /help')
