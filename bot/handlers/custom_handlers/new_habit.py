import datetime

from telebot.types import CallbackQuery, Message
from telegram_bot_calendar import LSTEP

from keyboards.reply import calendar_markup
from loader import bot
from request_to_api.habits_api import request_to_new_habit
from request_to_api.users_api import get_user_by_tg_id
from states.habit_info import HabitInfoState
from utils.calendar import MyStyleCalendar


@bot.message_handler(commands=["new_habit"])
def new_habit(message: Message) -> None:
    """
    Создание новой привычки
    :param message: Message - команда /new_habit
    :return: None
    """
    bot.set_state(message.from_user.id, HabitInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, "Введите название для вашей привычки: ")


@bot.message_handler(state=HabitInfoState.name)
def get_name(message: Message) -> None:
    """
    Получение названия привычки
    :param message: Message - название привычки
    :return: None
    """
    if not message.text.isdigit():
        bot.send_message(message.from_user.id, "Название записано. Введите описание: ")
        bot.set_state(message.from_user.id, HabitInfoState.description, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["name"] = message.text
    else:
        bot.send_message(
            message.from_user.id, "Название привычки не может состоять только из цифр!"
        )


@bot.message_handler(state=HabitInfoState.description)
def get_description(message: Message) -> None:
    """
    Получение описания привычки
    :param message: Message - описание привычки
    :return: None
    """
    bot.send_message(
        message.from_user.id,
        "Описание добавлено.\nВведите кол-во дней для выполнения, поставленной цели (настоятельно рекомендую выбирать не менее 21 дня): ",
    )
    bot.set_state(message.from_user.id, HabitInfoState.target_days, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["description"] = message.text


@bot.message_handler(state=HabitInfoState.target_days)
def get_target_days(message: Message) -> None:
    """
    Какая цель по дням
    :param message: Message - количество дней
    :return: None
    """
    bot.send_message(
        message.from_user.id,
        "Количество дней записал! Выберите дату начала выполнения привычки ",
        reply_markup=calendar_markup(),
    )
    bot.set_state(message.from_user.id, HabitInfoState.start_date, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["target_days"] = message.text


@bot.callback_query_handler(
    state=HabitInfoState.start_date, func=MyStyleCalendar.func(calendar_id=1)
)
def get_start_date(message: CallbackQuery) -> None:
    """
    Получение даты начала выполнения привычки
    :param message: CallbackQuery - дата начала
    :return: None
    """
    result, key, step = MyStyleCalendar(
        calendar_id=1, min_date=datetime.date.today()
    ).process(message.data)
    if not result and key:
        bot.edit_message_text(
            f"Select {LSTEP[step]}",
            message.message.chat.id,
            message.message.message_id,
            reply_markup=key,
        )
    elif result:
        with bot.retrieve_data(message.from_user.id) as data:
            data["start_date"] = result.isoformat()
            data["user_id"] = get_user_by_tg_id(message.from_user.id).get("id")
            bot.edit_message_text(
                f"Дата начала: {result}",
                message.message.chat.id,
                message.message.message_id,
            )
        response = request_to_new_habit(data)
        if response:
            text = (
                "\n*Название:* {name}"
                "\n*Описание:* {description}"
                "\n*Дата начала:* {start}"
                "\n*Количество дней для выполнения:* {target_days}"
            ).format(
                name=data.get("name"),
                description=data.get("description"),
                target_days=data.get("target_days"),
                start=result.isoformat(),
            )
            bot.send_message(message.from_user.id, "Привычка создана!👍")
        else:
            text = "Ошибка"
        bot.send_message(message.from_user.id, text, parse_mode="Markdown")
