from urllib.parse import urljoin

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo

from config import config


web_app_kb = InlineKeyboardBuilder()
web_app_kb.button(text="Try", web_app=WebAppInfo(url=urljoin(config.WEBAPP_URL, "/webapp")))


approve_pair = InlineKeyboardBuilder()
approve_pair.button(text="Да", callback_data="approve_pair")
approve_pair.button(text="Нет", callback_data="delete_pair")
