import logging
import asyncio
from configs import config
from aiogram import Bot, Dispatcher
from handlers import common, converter, converter_text


async def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_router(common.router)
    dp.include_router(converter.router)
    dp.include_router(converter_text.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())
