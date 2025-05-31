from keyboards import inline as inline_keyboard
from loader import bot
from request_to_api.habits_api import request_to_get_all_active_habits
from telebot.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


@bot.message_handler(commands=["list_habits"])
def show_list_habits(message: Message, edit: bool = False) -> None:
    """
    Просмотр списка всех действующих привычек
    :param message: команда /list_habits
    :param edit: редактируемое ли сообщение, по умолчанию False
    :return: None
    """
    if edit:
        user_tg_id = message.chat.id
    else:
        user_tg_id = message.from_user.id
    response = request_to_get_all_active_habits(user_tg_id=user_tg_id)
    if response:
        response = [
            {"text": i_btn["name"], "callback_data": "habit_" + str(i_btn["id"])}
            for i_btn in response
        ]
        text = "Ваши действующие привычки: "
        markup = inline_keyboard.gen_inline_markup(response)
        if edit:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.message_id,
                text=text,
                reply_markup=markup,
            )
        else:
            bot.send_message(
                message.from_user.id,
                text=text,
                reply_markup=markup,
            )
    else:
        text = "*Вы еще не добавили ни одной привычки*"
        if edit:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.message_id,
                text=text,
                parse_mode="Markdown",
            )
        else:
            bot.send_message(
                message.from_user.id,
                text,
                parse_mode="Markdown",
            )


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data.startswith("habit_"))
)
def handle_habit_selection(callback_query: CallbackQuery, edit: bool = False) -> None:
    """
    Обработчик, предоставляет Inline клавиатуру, для выбора действия с привычкой
    :param callback_query: запрос начинающийся на habit_ или back_to_crud_
    :param edit: Если True - то значит id будет лежать по индексу 3, иначе 1
    :return: None
    """
    if edit:
        habit_id = callback_query.data.split("_")[3]
    else:
        habit_id = callback_query.data.split("_")[1]
    actions_keyboard = InlineKeyboardMarkup(row_width=2)
    actions_keyboard.add(
        InlineKeyboardButton(text="Описание", callback_data=f"description_{habit_id}"),
        InlineKeyboardButton(text="Редактировать", callback_data=f"edit_{habit_id}"),
        InlineKeyboardButton(text="Удалить", callback_data=f"delete_{habit_id}"),
        InlineKeyboardButton(
            text="Отметить выполненной", callback_data=f"mark_{habit_id}"
        ),
        InlineKeyboardButton(text="🔙Назад", callback_data="back_to_list_habits"),
    )
    bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Выберите действие:",
        reply_markup=actions_keyboard,
    )
