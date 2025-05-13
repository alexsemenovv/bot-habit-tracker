import datetime

import requests

API_URL = "http://127.0.0.1:8000/api/habits_track"  # Адрес FastAPI


def request_to_mark_habit_by_id(habit_id: int) -> bool:
    """
    Запрос на отметку о выполнении привычки сегодня
    :param habit_id: int - id привычки
    :return: True - если отмечена, иначе False
    """
    habit = {"habit_id": habit_id, "date_of_completion": datetime.date.today().isoformat()}
    response = requests.post(API_URL, json=habit)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return False
