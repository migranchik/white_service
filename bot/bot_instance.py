from aiogram import Bot
from configs.settings import settings

if not settings.bot_token:
    raise RuntimeError("Please set BOT_TOKEN")

bot = Bot(token=settings.bot_token)
