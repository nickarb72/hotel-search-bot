from telebot import TeleBot
from telebot.storage import StateMemoryStorage

from config_data.config import BotSettings

user_data = {}
bot_settings = BotSettings()
bot_token = bot_settings.BOT_TOKEN.get_secret_value()
storage = StateMemoryStorage()
bot = TeleBot(token=bot_token, state_storage=storage)
