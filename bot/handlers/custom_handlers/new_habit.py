from datetime import datetime

from telebot.types import Message

from loader import bot
from request_to_api.users_api import get_user_by_tg_id
from states.habit_info import HabitInfoState
from request_to_api.habits_api import request_to_new_habit


@bot.message_handler(commands=['new_habit'])
def new_habit(message: Message) -> None:
    """Создание новой привычки"""
    bot.set_state(message.from_user.id, HabitInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, "Введите название для вашей привычки: ")


@bot.message_handler(state=HabitInfoState.name)
def get_name(message: Message) -> None:
    """Получение названия привычки"""
    if not message.text.isdigit():  # проверка, что введены не просто какие-то цифры
        bot.send_message(message.from_user.id, 'Название записано. Введите описание: ')
        bot.set_state(message.from_user.id, HabitInfoState.description, message.chat.id) #  меняем состояние

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data: # добавляем в класс состояния - название
            data['name'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Название привычки не может состоять только из цифр!')


@bot.message_handler(state=HabitInfoState.description)
def get_description(message: Message) -> None:
    """Получение описания привычки"""
    bot.send_message(message.from_user.id, 'Описание добавлено. Введите дату начала выполнения привычки, в формате YYYY-MM-DD: ')
    bot.set_state(message.from_user.id, HabitInfoState.start_date, message.chat.id)  # меняем состояние

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:  # добавляем в класс состояния - описание
        data['description'] = message.text


@bot.message_handler(state=HabitInfoState.start_date)
def get_start_date(message: Message) -> None:
    """Получение даты начала выполнения привычки"""
    start = datetime.strptime(message.text, "%Y-%m-%d").isoformat()
    bot.send_message(message.from_user.id, 'Дата начала записана!')

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:  # добавляем в класс состояния - дату начала
        data['start_date'] = start
        data['user_id'] = get_user_by_tg_id(message.from_user.id).get('id')
    result = request_to_new_habit(data)
    if result:
        text = f"Привычка создана!\nНазвание привычки: {data['name']}\nОписание: {data['description']}\nДата начала: {message.text}"
    else:
        text = "Ошибка"
    bot.send_message(message.from_user.id, text)

