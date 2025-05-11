from handlers.custom_handlers.list_habits import gen_inline_markup, handle_habit_selection
from loader import bot
from request_to_api.habits_api import (
    request_to_get_habit_by_id,
    request_to_delete_habit_by_id, request_to_get_all_active_habits,
)
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton


def gen_inline_markup_for_back_to_crud() -> InlineKeyboardMarkup:
    """
    Создание Inline клавиатуры для кнопки 'Назад к действиям'
    :return: клавиатуру InlineKeyboardMarkup
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="🔙Назад", callback_data="back_to_crud"),
    )
    return keyboard


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
    info = (
        "*Привычка* №{id}"
        "\n*Название:* {name}"
        "\n*Описание:* {description}"
        "\n*Дата начала:* {start}"
        "\n*Дней для выполнения:* {target_days}"
    ).format(
        id=habit.get("id"),
        name=habit.get("name"),
        description=habit.get("description"),
        target_days=habit.get("target_days"),
        start=habit.get("start_date"),
    )

    bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=info,
        reply_markup=gen_inline_markup_for_back_to_crud(),
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
    result = request_to_delete_habit_by_id(habit_id)
    if result:
        bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Привычка удалена!",
        )
    else:
        bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Ошибка запроса",
        )


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data == "back_to_list_habits")
)
def handle_btn_back(callback_query: CallbackQuery) -> None:
    """
    При нажатии на кнопку 'назад' - возвращает список привычек
    :param callback_query: CallbackQuery - запрос, который равен 'back_to_list_habits'
    :return: None
    """
    response = request_to_get_all_active_habits()
    if response:
        bot.send_message(
            callback_query.from_user.id,
            "Ваши действующие привычки: ",
            reply_markup=gen_inline_markup(response),
        )
    else:
        bot.send_message(
            callback_query.from_user.id,
            "*Вы еще не добавили ни одной привычки*",
            parse_mode="Markdown",
        )


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data == "back_to_crud")
)
def handle_btn_back(callback_query: CallbackQuery) -> None:
    """
    При нажатии на кнопку 'назад' - возвращает список действий для привычки
    :param callback_query: CallbackQuery - запрос, который равен на 'back_to_crud'
    :return: None
    """
    handle_habit_selection(callback_query)
