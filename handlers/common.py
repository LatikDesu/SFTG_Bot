from aiogram import Router
from aiogram.dispatcher.filters.command import Command
from aiogram.types import Message
from keyboards.main_menu import get_menu_kb

router = Router()


@router.message(Command(commands=["start", "help"]))
async def cmd_start(message: Message):
    await message.answer("Я бот-помощник, могу для Вас произвести конвертацию валюты /convert \n"
                         "Список доступных валют /values \n"
                         "Можно ввести текстом <валюта, цену которой нужно узнать> <валюта, в которой надо узнать цену> <количество валюты>", reply_markup=get_menu_kb())
