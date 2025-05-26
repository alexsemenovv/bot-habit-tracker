from telebot.handler_backends import State, StatesGroup


class HabitInfoState(StatesGroup):
    """Состояния для полей привычки"""

    name = State()
    description = State()
    start_date = State()
    target_days = State()
    update_start_date = State()
