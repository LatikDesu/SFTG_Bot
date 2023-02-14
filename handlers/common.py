from aiogram import Router
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.main_menu import get_menu_kb

router = Router()


@router.message(Command(commands=["start", "help"]))
async def cmd_start(message: Message):
    await message.answer("Я бот-помощник по конвертации валюты \n"
                         "Произвести конвертацию валюты /convert \n"
                         "Список доступных валют /values \n"
                         "Отмена действия /cancel или 'отмена' \n"
                         "Можно ввести текстом <валюта, цену которой нужно узнать> <валюта, в которой надо узнать цену> <количество валюты>", reply_markup=get_menu_kb())


@router.message(Command(commands=["cancel"]))
@router.message(Text(text="отмена", text_ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Действие отменено", reply_markup=ReplyKeyboardRemove())
