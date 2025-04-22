from typing import Dict

import requests

API_URL = "http://127.0.0.1:8000/api/habits"  # Адрес FastAPI


def request_to_new_habit(habit: Dict) -> bool:
    """Отправка запроса на добавление новой привычке"""
    response = requests.post(API_URL, json=habit)
    if response.status_code == 200:
        return True
    return False
