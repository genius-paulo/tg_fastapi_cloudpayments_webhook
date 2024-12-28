from aiogram import types, Dispatcher, Bot
import payment_processing
from payment_processing import Payment
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer('Hi! The bot is working.')


@dp.message_handler(commands=["get_payment"])
async def get_payment_link(message: types.Message):
    # Сюда нужно передавать сумму из сообщения
    payment_link = await payment_processing.get_payment_link(10.0, 'USD', message.from_id)
    await message.answer(payment_link)


# Действия при удачной оплате
async def payment_received(payment: Payment):

    # Действия при успешной оплате

    # Сообщение для понимания, что платеж прошел успешно
    await bot.send_message(payment.account_id,
                           f'the payment {payment.invoice_id} was successful.'
                           f'\nThe amount: {payment.payment_amount}.')


# Действия при неудачной оплате
async def payment_cancellation(payment: Payment):

    # Действия при отмене оплаты

    # Сообщение для понимания, что платеж прошел с ошибкой
    await bot.send_message(payment.account_id,
                           f'The payment {payment.invoice_id} was made with an error.'
                           f'\nThe amount of {payment.payment_amount} 10 has not been credited.'
                           f'\nReason: {payment.cancel_reason}')
