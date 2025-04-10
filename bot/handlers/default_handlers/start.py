from telebot.types import Message

from main import bot
from request_to_api.users_api import (
    get_user_by_tg_id,
    add_user_with_api,
)


@bot.message_handler(commands=['start'])
def start(message: Message):
    """Функция, которая обрабатывает команду /start"""
    tg_id: int = message.from_user.id # вытаскиваем TG id
    response: bool = get_user_by_tg_id(tg_id) # получаем пользователя по id в БД
    if not response: # если пользователя нет, то добавляем его в БД
        data = {
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "username": message.from_user.username,
            "tg_id": message.from_user.id,
            "is_bot": message.from_user.is_bot,
        }
        add_user_with_api(data)
    bot.send_message(message.chat.id,
                     f"Привет, {message.from_user.full_name}! Это Бот.\nЯ умею отслеживать выполнение твоих привычек.")
