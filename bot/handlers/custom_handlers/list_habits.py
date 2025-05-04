from loader import bot
from request_to_api.habits_api import request_to_get_all_active_habits
from telebot.types import Message


@bot.message_handler(commands=["list_habits"])
def show_list_habits(message: Message) -> None:
    """Просмотр списка всех действующих привычек"""
    bot.send_message(message.from_user.id, "Ваши действующие привычки: ")
    response = request_to_get_all_active_habits()
    if response:
        for i_habit in response:
            info = "{id}) *Название:* {name}\n*Описание:* {description}\n*Дата начала:* {start}".format(
                id=i_habit.get("id"),
                name=i_habit.get("name"),
                description=i_habit.get("description"),
                start=i_habit.get("start_date"),
            )

            bot.send_message(message.from_user.id, info, parse_mode="Markdown")
