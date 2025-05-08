from telebot.types import CallbackQuery

from loader import bot
from request_to_api.habits_api import request_to_get_habit_by_id


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data.startswith("description_"))
)
def handle_description_habit(callback_query: CallbackQuery):
    """
    Обработчик, предоставляет привычки
    :param callback_query: CallbackQuery - запрос, который начинается на 'description_'
    :return: описание привычки
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

    bot.send_message(callback_query.from_user.id, info, parse_mode="Markdown")
