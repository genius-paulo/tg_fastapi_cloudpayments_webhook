import bot_processing
from fastapi import FastAPI, Request
from aiogram import types, Dispatcher, Bot

import payment_processing
from bot_processing import bot, dp
from time import sleep
from asyncio import sleep as asleep
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
NGROK_URL = os.getenv('NGROK_URL')
WEBHOOK_PATH = f"/bot/{TOKEN}"
WEBHOOK_URL = f"{NGROK_URL}{WEBHOOK_PATH}"
SKIP_UPDATES = os.getenv('SKIP_UPDATES')

app = FastAPI()


# Устанавливает WEBHOOK URL при запуске
@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )
    # Реализация skip_updates
    if SKIP_UPDATES:
        await bot.delete_webhook(drop_pending_updates=True)
        sleep(1)
        await asleep(0)
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


# Доставляет изменения боту при получении POST запроса от Telegram API
@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


# Закрывает сессию бота и удаляет вебхук
@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    session = await bot.get_session()
    await session.close()


# Хук для успешной оплаты CloudPayments
@app.post("/pay")
async def receive_webhook(request: Request):
    payment = await payment_processing.get_payment_parameters(request)
    await bot_processing.payment_received(payment)


# Хук для ошибки оплаты CloudPayments
@app.post("/fail")
async def receive_webhook(request: Request):
    payment = await payment_processing.get_payment_parameters(request)
    await bot_processing.payment_cancellation(payment)
