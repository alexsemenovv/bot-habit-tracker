from telebot.types import CallbackQuery, Message

from keyboards import inline as inline_keyboard
from loader import bot
from request_to_api.habits_api import (
    request_to_get_habit_by_id, request_to_update_habit_by_id,
)

# Словарь для хранения состояний (можно заменить на FSM или хранилище)
user_habit_edit_state = {}  # user_id: habit_id


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data.startswith("edit_"))
)
def handle_edit_habit(callback_query: CallbackQuery) -> None:
    """
    Обработчик, предоставляет поля для редактирования привычки
    :param callback_query: CallbackQuery - запрос, который начинается на 'edit_'
    :return: None
    """
    habit_id = int(callback_query.data.split("_")[1])
    buttons = [
        {"text": "Название", "callback_data": "update_name_" + str(habit_id)},
        {"text": "Описание", "callback_data": "update_description_" + str(habit_id)},
        {"text": "Дата начала", "callback_data": "update_start_date_" + str(habit_id)},
        {"text": "Количество дней для выполнения", "callback_data": "update_target_days_" + str(habit_id)},
        {"text": "🔙Назад", "callback_data": "back_to_crud_" + str(habit_id)},
    ]
    bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Выберите поле для редактирования",
        reply_markup=inline_keyboard.gen_inline_markup(buttons=buttons, row_width=1),
    )


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data.startswith("update_name_"))
)
def handle_edit_name_habit(callback_query: CallbackQuery) -> None:
    """
    Обработчик, предоставляет поле для редактирования названия привычки
    :param callback_query: CallbackQuery - запрос, который начинается на 'edit_name_'
    :return: None
    """
    habit_id = int(callback_query.data.split("_")[2])
    user_id = callback_query.from_user.id
    habit = request_to_get_habit_by_id(habit_id)
    user_habit_edit_state[user_id] = habit_id

    text = f"Текущее название привычки: *{habit['name']}*\nВведите новое название:"
    buttons = [{"text": "Отмена", "callback_data": "edit_" + str(habit_id)}]
    markup = inline_keyboard.gen_inline_markup(buttons=buttons, row_width=1)

    bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=markup,
        parse_mode="Markdown"
    )

    bot.register_next_step_handler_by_chat_id(
        callback_query.message.chat.id, process_new_habit_name
    )


def process_new_habit_name(message: Message) -> None:
    user_id = message.from_user.id
    if user_id not in user_habit_edit_state:
        bot.send_message(message.chat.id, "Что-то пошло не так. Попробуйте снова.")
        return

    new_name = {"name": message.text.strip()}

    result = request_to_update_habit_by_id(habit_id=user_habit_edit_state[user_id], fields=new_name)
    if result:
        bot.send_message(message.chat.id, f"Название привычки обновлено на: *{new_name.get('name')}*",
                         parse_mode="Markdown")
    else:
        bot.send_message(message.from_user.id, "Не получилось обновить привычку...")
    # Здесь можно вернуть пользователя назад в меню редактирования



