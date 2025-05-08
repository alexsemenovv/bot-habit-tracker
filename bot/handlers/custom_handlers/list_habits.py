from typing import List

from loader import bot
from request_to_api.habits_api import request_to_get_all_active_habits
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup


def gen_inline_markup(buttons: List[dict]) -> InlineKeyboardMarkup:
    """
    Создание Inline клавиатуры
    :param buttons: List  - список названий кнопок
    :return: клавиатуру InlineKeyboardMarkup
    """
    buttons = [InlineKeyboardButton(text=i_btn["name"], callback_data=i_btn["name"]) for i_btn in buttons]
    keyboard =  InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard



@bot.message_handler(commands=["list_habits"])
def show_list_habits(message: Message) -> None:
    """Просмотр списка всех действующих привычек"""
    response = request_to_get_all_active_habits()
    if response:
        bot.send_message(message.from_user.id, "Ваши действующие привычки: ", reply_markup=gen_inline_markup(response))
    else:
        bot.send_message(message.from_user.id, "*Вы еще не добавили ни одной привычки*", parse_mode="Markdown")



