from configs import APIException, Convertor
from aiogram.types import Message
from aiogram import Router
import traceback
import sys
sys.path.append("..")


router = Router()


@router.message(content_types="text")
async def convert_text(message: Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверная команда!')

        answer = Convertor.get_price(*values)

    except APIException as e:
        await message.answer(f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        await message.answer(f"Неизвестная ошибка:\n{e}")
    else:
        await message.answer(answer)
