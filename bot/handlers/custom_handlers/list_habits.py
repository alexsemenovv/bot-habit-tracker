from typing import List

from loader import bot
from request_to_api.habits_api import request_to_get_all_active_habits
from telebot.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)


def gen_inline_markup(buttons: List[dict]) -> InlineKeyboardMarkup:
    """
    Создание Inline клавиатуры
    :param buttons: List  - список названий кнопок
    :return: клавиатуру InlineKeyboardMarkup
    """
    buttons = [
        InlineKeyboardButton(
            text=i_btn["name"], callback_data="habit_" + str(i_btn["id"])
        )
        for i_btn in buttons
    ]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


@bot.message_handler(commands=["list_habits"])
def show_list_habits(message: Message) -> None:
    """Просмотр списка всех действующих привычек"""
    response = request_to_get_all_active_habits()
    if response:
        bot.send_message(
            message.from_user.id,
            "Ваши действующие привычки: ",
            reply_markup=gen_inline_markup(response),
        )
    else:
        bot.send_message(
            message.from_user.id,
            "*Вы еще не добавили ни одной привычки*",
            parse_mode="Markdown",
        )


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data.startswith("habit_"))
)
def handle_habit_selection(callback_query: CallbackQuery):
    """Обработчик, предоставляет Reply клавиатуру, для выбора действия с привычкой"""

    habit_id = callback_query.data.split("_")[1]
    actions_keyboard = InlineKeyboardMarkup(row_width=2)
    actions_keyboard.add(
        InlineKeyboardButton(text="Описание", callback_data=f"description_{habit_id}"),
        InlineKeyboardButton(text="Редактировать", callback_data=f"edit_{habit_id}"),
        InlineKeyboardButton(text="Удалить", callback_data=f"delete_{habit_id}"),
        InlineKeyboardButton(
            text="Отметить выполненной", callback_data=f"mark_{habit_id}"
        ),
        InlineKeyboardButton(text="🔙Назад", callback_data=f"back"),
    )

    bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Выберите действие:",
        reply_markup=actions_keyboard,
    )
