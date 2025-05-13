from typing import Dict, List

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def gen_inline_markup(
    buttons: List[Dict[str, str]],
) -> InlineKeyboardMarkup:
    """
    Создание Inline клавиатуры
    :param buttons: List - Список с названиями кнопок, и callback_data
    :return: клавиатуру InlineKeyboardMarkup
    """
    buttons = [
        InlineKeyboardButton(text=i_btn["text"], callback_data=i_btn["callback_data"])
        for i_btn in buttons
    ]

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard
