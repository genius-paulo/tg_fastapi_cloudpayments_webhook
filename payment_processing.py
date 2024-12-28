from fastapi import Request
from pydantic import BaseModel
import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()

CP_PUBLIC_ID = os.getenv('CP_PUBLIC_ID')
API_PASSWORD = os.getenv('API_PASSWORD')


class Payment(BaseModel):
    account_id: str | None = None
    payment_amount: str | None = None
    invoice_id: str | None = None
    cancel_reason: str | None = None


# Функция для того, чтобы разложить платежную ссылочку на нужные нам параметры и забить все это дело в объект
async def get_payment_parameters(request: Request) -> Payment:
    # Получаем запрос
    data = await request.body()
    # Разбиваем запрос на параметры по &
    parameters = data.decode('utf-8').split('&')
    payment = Payment()
    for parameter in parameters:
        if 'AccountId' in parameter:
            payment.account_id = parameter.split('=')[1]
        elif 'PaymentAmount' in parameter:
            payment.payment_amount = parameter.split('=')[1]
        elif 'InvoiceId' in parameter:
            payment.invoice_id = parameter.split('=')[1]
        elif 'Reason=' in parameter:
            payment.cancel_reason = parameter.split('=')[1]
    return payment


async def get_payment_link(amount: float | int, currency: str, user_id: int) -> str:
    # Авторизуемся и заполняем data для Cloud Payments
    auth_header = "Basic " + base64.b64encode(str(CP_PUBLIC_ID + ':' + API_PASSWORD).encode()).decode()
    headers = {"Authorization": auth_header}
    data = {
        "Amount": amount,
        "Currency": currency,
        "Description": "Top up your account",
        "RequireConfirmation": 'true',
        "SendEmail": 'false',
        # Передаем AccountId, чтобы получить его обратно через вебхук и понять, кому зачислять платеж
        "AccountId": str(user_id),
    }
    # Генерируем платежную ссылку
    try:
        response = requests.post('https://api.cloudpayments.ru/orders/create', headers=headers, data=data)
        payment_link = response.json()['Model']['Url']
        return payment_link
    except Exception as e:
        return f'Error: {e}'
