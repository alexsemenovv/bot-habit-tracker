from typing import Dict, List

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def gen_inline_markup(
        buttons: List[Dict[str, str]],
        row_width: int = 2,
) -> InlineKeyboardMarkup:
    """
    Создание Inline клавиатуры
    :param
        buttons: List - Список с названиями кнопок, и callback_data
        row_width: int - количество кнопок в одной строке. По умолчанию 2
    :return: клавиатуру InlineKeyboardMarkup
    """
    buttons = [
        InlineKeyboardButton(text=i_btn["text"], callback_data=i_btn["callback_data"])
        for i_btn in buttons
    ]

    keyboard = InlineKeyboardMarkup(row_width=row_width, )
    keyboard.add(*buttons)
    return keyboard
