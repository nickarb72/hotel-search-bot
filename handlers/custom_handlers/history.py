from telebot.types import Message
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date, timedelta

from loader import bot
from states.history import HistoryStates


@bot.message_handler(commands=["history"])
def get_history(message: Message) -> None:
    bot.set_state(message.from_user.id, HistoryStates.query_date, message.chat.id)
    bot.send_message(message.from_user.id, "Введите дату для поиска истории запросов.")
    calendar, step = DetailedTelegramCalendar(
        min_date=date.today() - timedelta(days=365),
        max_date=date.today()
    ).build()
    bot.send_message(message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)

