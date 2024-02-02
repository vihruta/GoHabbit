from dataclasses import dataclass


@dataclass(frozen=True)
class ButtonPhrases:
    week_subscription = "На неделю: 99₽"
    month_subscription = "На месяц: 249₽ (экономия 40%)"
    quarter_subscription = 'На 3 месяца: 599₽ (экономия 60%)'
    promocode_text = 'У меня есть промокод'
    week_price = '99'
    month_price = '249'
    quarter_price = '599'

    subscription_confirm = {'week': 'Подписка на неделю оплачена',
                            'month': 'Подписка на месяц оплачена',
                            'quarter': 'Подписка на 3 месяца оплачена'
                            }
    payment_faq = "После оплаты необходимо нажать на кнопку " \
                  "<b>'Проверить оплату'</b>"
    pay_text = 'Оплатить подписку'
    pay_check = 'Проверить оплату'
    water = 'Вода'
    sleep = 'Сон'
    drugs = 'Таблетки'
    confirmation = 'Да'
    decline = 'Нет'
