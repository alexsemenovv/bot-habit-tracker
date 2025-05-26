import datetime

from telebot.types import CallbackQuery, Message, InlineKeyboardMarkup
from telegram_bot_calendar import LSTEP

from keyboards import inline as inline_keyboard
from keyboards.reply import calendar_markup
from loader import bot
from request_to_api.habits_api import (
    request_to_get_habit_by_id, request_to_update_habit_by_id,
)
from states.habit_info import HabitInfoState
from utils.calendar import MyStyleCalendar


def get_edit_habit_markup(habit_id: int) -> InlineKeyboardMarkup:
    """
    Создание inline клавиатуры для редактирования привычки
    :param habit_id: int - id привычки
    :return: клавиатура Inline
    """
    buttons = [
        {"text": "Название", "callback_data": f"update_name_{habit_id}"},
        {"text": "Описание", "callback_data": f"update_description_{habit_id}"},
        {"text": "Дата начала", "callback_data": f"update_start_date_{habit_id}"},
        {"text": "Количество дней для выполнения", "callback_data": f"update_target_days_{habit_id}"},
        {"text": "🔙Назад", "callback_data": f"back_to_crud_{habit_id}"},
    ]
    return inline_keyboard.gen_inline_markup(buttons=buttons, row_width=1)


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
    bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Выберите поле для редактирования",
        reply_markup=get_edit_habit_markup(habit_id),
    )


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data.startswith("update_name_"))
)
def handle_update_name_habit(callback_query: CallbackQuery) -> None:
    """
    Обработчик, предоставляет поле для редактирования названия привычки
    :param callback_query: CallbackQuery - запрос, который начинается на 'update_name_'
    :return: None
    """
    habit_id = int(callback_query.data.split("_")[2])
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    habit = request_to_get_habit_by_id(habit_id)

    bot.set_state(user_id, HabitInfoState.name, chat_id)
    with bot.retrieve_data(user_id, chat_id) as data:
        data["habit_id"] = habit_id

    text = f"Текущее название привычки: *{habit['name']}*\nВведите новое название:"
    buttons = [{"text": "Отмена", "callback_data": f"edit_{str(habit_id)}"}]
    markup = inline_keyboard.gen_inline_markup(buttons=buttons, row_width=1)

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=markup,
        parse_mode="Markdown"
    )

    bot.register_next_step_handler_by_chat_id(
        chat_id, process_new_habit_name
    )


@bot.message_handler(state=HabitInfoState.name)
def process_new_habit_name(message: Message) -> None:
    """
    Получение нового названия для привычки
    :param message: Message - новое название для привычки
    :return: None
    """
    user_id = message.from_user.id
    chat_id = message.chat.id
    with bot.retrieve_data(user_id, chat_id) as data:
        habit_id = data["habit_id"]

    new_name = {"name": message.text.strip()}

    result = request_to_update_habit_by_id(habit_id=habit_id, fields=new_name)
    if result:
        bot.send_message(chat_id, f"Название привычки обновлено на: *{new_name.get('name')}*",
                         parse_mode="Markdown")
    else:
        bot.send_message(message.from_user.id, "Не получилось обновить привычку...")

    bot.delete_state(user_id, chat_id)

    bot.send_message(
        chat_id,
        "Выберите поле для редактирования:",
        reply_markup=get_edit_habit_markup(habit_id),
    )


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data.startswith("update_description_"))
)
def handle_update_description_habit(callback_query: CallbackQuery) -> None:
    """
    Обработчик, предоставляет поле для редактирования описания привычки
    :param callback_query: CallbackQuery - запрос, который начинается на 'update_description_'
    :return: None
    """
    habit_id = int(callback_query.data.split("_")[2])
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    habit = request_to_get_habit_by_id(habit_id)

    bot.set_state(user_id, HabitInfoState.description, chat_id)
    with bot.retrieve_data(user_id, chat_id) as data:
        data["habit_id"] = habit_id

    text = f"Текущее описание привычки: *{habit['description']}*\nВведите новое описание:"
    buttons = [{"text": "Отмена", "callback_data": f"edit_{str(habit_id)}"}]
    markup = inline_keyboard.gen_inline_markup(buttons=buttons, row_width=1)

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=markup,
        parse_mode="Markdown"
    )

    bot.register_next_step_handler_by_chat_id(
        chat_id, process_new_habit_description
    )


@bot.message_handler(state=HabitInfoState.description)
def process_new_habit_description(message: Message) -> None:
    """
    Получение нового описания для привычки
    :param message: Message - новое описание для привычки
    :return: None
    """
    user_id = message.from_user.id
    chat_id = message.chat.id
    with bot.retrieve_data(user_id, chat_id) as data:
        habit_id = data["habit_id"]

    new_desc = {"description": message.text.strip()}

    result = request_to_update_habit_by_id(habit_id=habit_id, fields=new_desc)
    if result:
        bot.send_message(chat_id, f"Описание привычки обновлено на: *{new_desc.get('description')}*",
                         parse_mode="Markdown")
    else:
        bot.send_message(message.from_user.id, "Не получилось обновить привычку...")

    bot.delete_state(user_id, chat_id)

    bot.send_message(
        chat_id,
        "Выберите поле для редактирования:",
        reply_markup=get_edit_habit_markup(habit_id),
    )


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data.startswith("update_start_date_"))
)
def handle_update_start_date_habit(callback_query: CallbackQuery) -> None:
    """
    Обработчик, предоставляет календарь для редактирования начала выполнения привычки
    :param callback_query: CallbackQuery - запрос, который начинается на 'update_start_date_'
    :return: None
    """
    habit_id = int(callback_query.data.split("_")[3])
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    habit = request_to_get_habit_by_id(habit_id)

    bot.set_state(user_id, HabitInfoState.update_start_date, chat_id)
    with bot.retrieve_data(user_id, chat_id) as data:
        data["habit_id"] = habit_id

    text = f"Текущая дата начала выполнения привычки: *{habit['start_date']}*\nВыберите новую дату:"

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=calendar_markup(),
        parse_mode="Markdown"
    )


@bot.callback_query_handler(
    state=HabitInfoState.update_start_date, func=MyStyleCalendar.func(calendar_id=1)
)
def get_new_start_date(callback_query: CallbackQuery) -> None:
    """
    Получение новой даты начала выполнения привычки
    :param callback_query: CallbackQuery - дата начала
    :return: None
    """
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    result, key, step = MyStyleCalendar(
        calendar_id=1, min_date=datetime.date.today()
    ).process(callback_query.data)
    if not result and key:
        bot.edit_message_text(
            f"Select {LSTEP[step]}",
            chat_id,
            message_id=callback_query.message.message_id,
            reply_markup=key,
            parse_mode="Markdown"
        )
    elif result:
        with bot.retrieve_data(user_id, chat_id) as data:
            habit_id = data["habit_id"]
        new_start_date = {"start_date": result.isoformat()}

        result = request_to_update_habit_by_id(habit_id=habit_id, fields=new_start_date)
        if result:
            bot.send_message(chat_id,
                             f"Дата начала выполнения привычки обновлена на: *{new_start_date.get('start_date')}*",
                             parse_mode="Markdown")
        else:
            bot.send_message(user_id, "Не получилось обновить привычку...")

        bot.delete_state(user_id, chat_id)

        bot.send_message(
            chat_id,
            "Выберите поле для редактирования:",
            reply_markup=get_edit_habit_markup(habit_id),
        )
