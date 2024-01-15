from dataclasses import dataclass


@dataclass(frozen=True)
class AdminPhrases:
    admin = "Админка"
    give_access_button_text = "Выдать доступ"
    select_user_message_text = "Выберите пользователя"
    enter_access_expires_at_datetime_message_text = (
        "Введите дату и время истечения доступа в формате ДД.ММ.ГГГГ чч:мм"
    )
    select_user_button_text = "Выбрать пользователя"
    give_access_message_text = "Доступ выдан"
    bot_user_not_found_message_text = "Указанный пользователь не найден. Убедитесь, что он активировал бота, и попробуйте еще раз"
    remove_access_button_text = "Забрать доступ"
    remove_access_message_text = "Доступ отозван"
