import uuid
import logging

import yookassa
from yookassa import Configuration, Payment
from ..phrases.button_phrases import ButtonPhrases

TOKEN_API_ID = "280413"
TOKEN_API = 'live_VjcqtDfXfO9IkNzcswXtnqsxPyBZ3KZ5XbXKgHsxTgk'


def create_payment(price):
    Configuration.account_id = TOKEN_API_ID
    Configuration.secret_key = TOKEN_API
    logging.info('Запрос отправлен')
    payment = Payment.create({
        "amount": {
            "value": price,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/eruditgpt_bot"
        },
        "capture": True,
        "description": "Оплата подписки",
        "receipt": {
            "items": [
                {
                    "description": "Оплата подписки GoHabbit",
                    "quantity": "1.00",
                    "amount": {
                        "value": price,
                        "currency": "RUB"
                    },
                    "vat_code": 6
                }
            ],
            "email": "erudigtgpt.noreply@gmail.com"
        }
    }, uuid.uuid4())

    url = payment.confirmation.confirmation_url

    return url, payment.id


def check_pay(payment_id):
    payment = yookassa.Payment.find_one(payment_id)
    if payment.status == "succeeded":
        amount = float(payment.amount.value)
        if amount == float(ButtonPhrases.week_price):
            subscription_type = "week"
        elif amount == float(ButtonPhrases.month_price):
            subscription_type = "month"
        elif amount == float(ButtonPhrases.quarter_price):
            subscription_type = "quarter"
        else:
            subscription_type = False
    else:
        subscription_type = False
    return subscription_type
