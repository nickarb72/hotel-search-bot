import os

from dotenv import load_dotenv, find_dotenv
from pydantic import SecretStr, StrictStr
from pydantic_settings import BaseSettings


if not find_dotenv():
    exit("Переменные окружения не загружены т.к. отсутствует файл .env")
else:
    load_dotenv()

class BotSettings(BaseSettings):
    BOT_TOKEN: SecretStr = os.getenv("BOT_TOKEN", None)
    RAPID_API_KEY: SecretStr = os.getenv("RAPID_API_KEY", None)

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("get_accom_details", "Получить информацию о размещении"),
    ("lowprice", "Отображение топа 5-ти самых доступных отелей в указанной локации"),
    ("guest_rating", "Отображение топа 5-ти самых популярных отелей в указанной локации"),
    ("bestdeal", "Отображение топа 5-ти отелей, находящихся ближе всего к центру города"),
    ("history", "Отображение истории запросов поиска отелей за определенную дату"),
    ("help", "Вывести справку")
)
