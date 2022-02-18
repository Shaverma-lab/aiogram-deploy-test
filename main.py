from aiogram import Dispatcher, Bot, executor, types
import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import os

TOKEN = '5156487975:AAEA4IaC4ivT_08mMjame_ryhOM9-AngDpI'

WEBHOOK_HOST = 'https://aiogram-deploy-test.herokuapp.com/'
WEBHOOK_PATH = f'/wenhook/{TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.environ.get("PORT", 5000))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)

async def on_startup(dispatcher: Dispatcher) -> None:
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    await bot.delete_webhook()

    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')

if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )