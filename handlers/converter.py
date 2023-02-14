import requests
from aiogram import Router, F
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State
from keyboards.main_menu import get_menu_kb, get_exchange_kb
from configs import config, exchanges


router = Router()


class OrderExchange(StatesGroup):
    choosing_base_key = State()
    choosing_sym_key = State()
    calculation = State()


item_kb = list(exchanges.keys())


# Показать доступные валюты
@router.message(Command(commands=["values"]))
@router.message(Text(text="Доступные валюты"))
async def cmd_values(message: Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    await message.answer(text, reply_markup=get_menu_kb())


# Выбор валюты для конвертации
@router.message(Command(commands=["convert"]))
@router.message(Text(text="Конвертировать валюту"))
async def cmd_convert(message: Message, state: FSMContext):
    text = 'Выберите базовую валюту:'
    await message.answer(text, reply_markup=get_exchange_kb(item_kb))
    await state.set_state(OrderExchange.choosing_base_key)


@router.message(OrderExchange.choosing_base_key, F.text.in_(exchanges.keys()))
async def base_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_base=exchanges[message.text.lower()])
    item_kb.remove(message.text.lower())
    await message.answer("Теперь, выберите в какую валюту конвертировать:", reply_markup=get_exchange_kb(item_kb))
    await state.set_state(OrderExchange.choosing_sym_key)


# если валюта введена с клавиатуры и ее нет в списке
@router.message(OrderExchange.choosing_base_key)
async def base_chosen_incorrectly(message: Message):
    await message.answer(text="Я не знаю такой валюты.\n\n"
                         "Пожалуйста, выберите одно из списка ниже:", reply_markup=get_exchange_kb(item_kb))


# выбор валюты в которую конвертировать
@router.message(OrderExchange.choosing_sym_key, F.text.in_(exchanges.keys()))
async def sym_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_sym=exchanges[message.text.lower()])
    await message.answer("Введите количество валюты:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderExchange.calculation)


# если валюта введена с клавиатуры и ее нет в списке
@router.message(OrderExchange.choosing_sym_key)
async def sym_chosen_incorrectly(message: Message):
    await message.answer(text="Я не знаю такой валюты.\n\n"
                         "Пожалуйста, выберите одно из списка ниже:", reply_markup=get_exchange_kb(item_kb))


# ввод количетсва валюты
@router.message(OrderExchange.calculation, F.text.isdigit())
async def exchange_calc(message: Message, state: FSMContext):
    user_data = await state.get_data()
    r = requests.get(
        f"https://openexchangerates.org/api/latest.json?app_id={config.api_id.get_secret_value()}&base={user_data['chosen_base']}&symbols={user_data['chosen_sym']}").json()

    amount = float(message.text)
    answer = r['rates'][user_data['chosen_sym']]*amount
    item_kb.clear()
    item_kb.extend(list(exchanges.keys()))
    await message.answer(f"Цена {amount} {user_data['chosen_base']} в {user_data['chosen_sym']} = {answer}", reply_markup=get_menu_kb())
    await state.clear()


# если введено не число
@router.message(OrderExchange.calculation)
async def exchange_calc_incorrectly(message: Message):
    await message.answer(text="Введите число")
