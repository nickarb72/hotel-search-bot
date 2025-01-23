import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к. отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("get_accom_details", "Получить информацию о размещении"),
    ("lowprice", "Отображение топа 5-ти самых доступных отелей в указанной локации"),
    ("guest_rating", "Отображение топа 5-ти самых популярных отелей в указанной локации"),
    ("bestdeal", "Отображение топа 5-ти отелей, находящихся ближе всего к центру города"),
    ("help", "Вывести справку")
)
