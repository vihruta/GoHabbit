from dataclasses import dataclass

from .admin_phrases import AdminPhrases


@dataclass(frozen=True)
class BotPhrases:
    admin = AdminPhrases()
    bot_started = "Бот {me.username} успешно запущен"
    start_message_text = "Привет! Я - Эрудит, твой помощник в мире фриланса 💵\n\n" \
                         "Легкий доступ к ChatGPT без ограничений. " \
                         "Никаких VPN и регистраций! 🌐\n\n" \
                         "Я помогу тебе с созданием контента, анализом трендов" \
                         " и эффективной организацией работы. Используй меня " \
                         "для работы и повседневной жизни. Давай вместе " \
                         "достигать новых высот!\n\n" \
                         "<b>Без подписки у вас есть 10 бесплатных запросов.\n\n</b>" \
                         "🚀Если у меня возникнут трудности или я" \
                         "перестану отвечать, используй команду /start"
    no_access_message_text = "У вас нет доступа. Используйте /faq для справки"
    trial_end_text = 'Триал закончился! Для справки используйте /faq'
    invalid_content_type_message_text = "Неподдерживаемый тип данных"
    context_cleanup_message_text = "Ваш контекст очищен"
    retry_limit_exceeded_message_text = "Запрос не удался. Повторите запрос."
    faq_text = ''
    subscription_info = "Все варианты подписок подразумевают под собой <u>полный" \
                        " безлимит</u> как по количеству запросов, так и по " \
                        "токенам/символам"

    promo_confirm = 'Промокод применен. Ваша подписка активна до '
    promo_error_time = 'Действие промокода уже закончилось'
    promo_error = 'Неправильный промокод! Попробуйте еще раз!'\
                  '\n Для выхода используйте /start'
    water_first_answer = 'Ты выбрал привитие питья воды. \nДавай теперь ' \
                         'разберёмся, в какое время тебе стоит напоминать ' \
                         'попить воды. (в формате HH:MM, HH:MM...)' \
                         'количество напоминаний может быть любым'
    habit_date_accept = 'Все даты введены верно'
    habit_date_error = 'В какой-то из дат была ошибка. Попробуйте еще раз в ' \
                       'формате: "HH:MM, HH:MM..."'


phrases = BotPhrases()