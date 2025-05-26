from handlers.custom_handlers.list_habits import (
    handle_habit_selection,
    show_list_habits,
)
from keyboards import inline as inline_keyboard
from loader import bot
from request_to_api.habits_api import (
    request_to_delete_habit_by_id,
    request_to_get_habit_by_id,
)
from request_to_api.habits_track_api import (
    request_to_count_days_mark_habit,
    request_to_mark_habit_by_id,
)
from telebot.types import CallbackQuery


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data.startswith("mark_"))
)
def handle_mark_habit(callback_query: CallbackQuery) -> None:
    """
    Обработчик, отмечает привычку выполненной
    :param callback_query: CallbackQuery - запрос, который начинается на 'mark_'
    :return: None
    """
    habit_id = int(callback_query.data.split("_")[1])
    response = request_to_mark_habit_by_id(habit_id)
    if response:
        count_days = request_to_count_days_mark_habit(habit_id)
        text = f"Привычка на сегодня отмечена выполненной!👍\nТак держать💪\nУже выполненно дней: {count_days}"
    else:
        text = "Эта привычка уже отмечена выполненной сегодня!"
    bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
    )


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data.startswith("description_"))
)
def handle_description_habit(callback_query: CallbackQuery) -> None:
    """
    Обработчик, предоставляет описание привычки
    :param callback_query: CallbackQuery - запрос, который начинается на 'description_'
    :return: None
    """
    habit_id = int(callback_query.data.split("_")[1])
    habit = request_to_get_habit_by_id(habit_id)
    count_days = request_to_count_days_mark_habit(habit_id)
    info = (
        "*Привычка* №{id}"
        "\n*Название:* {name}"
        "\n*Описание:* {description}"
        "\n*Дата начала:* {start}"
        "\n*Дней для выполнения:* {target_days}"
        "\n*Уже выполнено дней:* {count_days}"
    ).format(
        id=habit.get("id"),
        name=habit.get("name"),
        description=habit.get("description"),
        target_days=habit.get("target_days"),
        start=habit.get("start_date"),
        count_days=count_days,
    )
    buttons = [{"text": "🔙Назад", "callback_data": "back_to_crud_" + str(habit_id)}]
    bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=info,
        reply_markup=inline_keyboard.gen_inline_markup(buttons=buttons),
        parse_mode="Markdown",
    )


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data.startswith("delete_"))
)
def handle_delete_habit(callback_query: CallbackQuery) -> None:
    """
    Обработчик, удаляет привычку
    :param callback_query: CallbackQuery - запрос, который начинается на 'delete_'
    :return: None
    """
    habit_id = int(callback_query.data.split("_")[1])
    buttons = [
        {"text": "Да", "callback_data": "yes_" + str(habit_id)},
        {"text": "Нет", "callback_data": "no_delete_habit_" + str(habit_id)},
    ]
    bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=f"Вы уверены что хотите удалить привычку?",
        reply_markup=inline_keyboard.gen_inline_markup(buttons=buttons),
    )


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data.startswith("yes_"))
)
def handle_yes_delete_habit(callback_query: CallbackQuery) -> None:
    """
    Удаление привычки по id
    :param callback_query: Запрос, который начинается на yes_
    :return: None
    """
    habit_id = int(callback_query.data.split("_")[1])
    result = request_to_delete_habit_by_id(habit_id)
    if result:
        bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Привычка удалена!\nСправка /help",
        )
    else:
        bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Ошибка запроса",
        )


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data.startswith("no_delete_habit_"))
)
def handle_no_delete_habit(callback_query: CallbackQuery) -> None:
    """
    Отмена удаления привычки по id
    :param callback_query: Запрос, который начинается на no_delete_habit_
    :return: None
    """
    handle_habit_selection(callback_query, edit=True)


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data == "back_to_list_habits")
)
def handle_btn_back_to_list_habits(callback_query: CallbackQuery) -> None:
    """
    При нажатии на кнопку 'назад' - возвращает список привычек
    :param callback_query: CallbackQuery - запрос, который равен 'back_to_list_habits'
    :return: None
    """
    show_list_habits(callback_query.message, edit=True)


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data.startswith("back_to_crud_"))
)
def handle_btn_back_to_crud(callback_query: CallbackQuery) -> None:
    """
    При нажатии на кнопку 'назад' - возвращает список действий для привычки
    :param callback_query: CallbackQuery - запрос, который начинается на 'back_to_crud'
    :return: None
    """
    handle_habit_selection(callback_query, edit=True)
