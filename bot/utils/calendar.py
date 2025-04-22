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
    TRANSLATION_DAYS_OF_WEEK = (
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
        self.locale = 'ru'
        self.days_of_week["ru"] = self.TRANSLATION_DAYS_OF_WEEK
        self.months["ru"] = self.TRANSLATION_MONTHS
