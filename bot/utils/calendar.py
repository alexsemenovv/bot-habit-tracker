from telegram_bot_calendar import DetailedTelegramCalendar


class MyStyleCalendar(DetailedTelegramCalendar):
    """Кастомный календарь для выбора даты"""

    TRANSLATION_MONTHS = (
        "Янв",
        "Фев",
        "Мар",
        "Апр",
        "Май",
        "Июнь",
        "Июль",
        "Авг",
        "Сен",
        "Окт",
        "Ноя",
        "Дек",
    )
    DAYS_OF_WEEK = (
        "Пн",
        "Вт",
        "Ср",
        "Чт",
        "Пт",
        "Сб",
        "Вс",
    )
    prev_button = "🔙"
    next_button = "🔜"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.days_of_week["yourtransl"] = self.DAYS_OF_WEEK
        self.months["yourtransl"] = self.TRANSLATION_MONTHS
