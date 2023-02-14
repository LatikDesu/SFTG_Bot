from configs import exchanges
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton


def get_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Конвертировать валюту")
    kb.button(text="Доступные валюты")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_exchange_kb() -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=key) for key in exchanges]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
