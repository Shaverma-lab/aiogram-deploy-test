from aiogram import Dispatcher, Bot, executor, types
import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import os
import psycopg2

TOKEN = '5156487975:AAEA4IaC4ivT_08mMjame_ryhOM9-AngDpI'

WEBHOOK_HOST = 'https://aiogram-deploy-test.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.environ.get("PORT", 5000))

DB_URI = 'postgres://zeggusrpjmigok:53f68d040e0bfea32968aac22c73b3a67d932b9f9665ef0923687317b257100c@ec2-3-228-236-221.compute-1.amazonaws.com:5432/daasq9dv4plgkh'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

db_connection = psycopg2.connect(DB_URI, sslmode='require')
db_object = db_connection.cursor()

@dp.message_handler()
async def echo(message: types.Message):
    db_object.execute(f"SELECT id FROM test_db WHERE user_id = {message.chat.id}")
    result = db_object.fetchone()
    print(result)
    if not result:
        db_object.execute(f"INSERT INTO test_db(user_id) VALUES (%s)", (message.chat.id,))
        db_connection.commit()

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