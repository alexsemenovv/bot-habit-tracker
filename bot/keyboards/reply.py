import datetime

from utils.calendar import MyStyleCalendar


def calendar_markup(cal_id: int = 1) -> tuple:
    """
    Создание клавиатуры с календарём
    :param cal_id: номер календаря(имеет смысл, если будет несколько календарей)
    :return: кортеж с датой
    """
    calendar, step = MyStyleCalendar(
        min_date=datetime.date.today(), calendar_id=cal_id
    ).build()
    return calendar
