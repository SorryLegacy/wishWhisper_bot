from urllib.parse import urljoin

from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import config

pair_keyboard = InlineKeyboardBuilder()
pair_keyboard.button(text="Try", web_app=WebAppInfo(url=urljoin(config.WEBAPP_URL, "/webapp")))


approve_pair = InlineKeyboardBuilder()
approve_pair.button(text="Да", callback_data="approve_pair")
approve_pair.button(text="Нет", callback_data="delete_pair")
