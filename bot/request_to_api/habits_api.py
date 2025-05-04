from typing import Dict, List

import requests

API_URL = "http://127.0.0.1:8000/api/habits"  # Адрес FastAPI


def request_to_new_habit(habit: Dict) -> bool:
    """Отправка запроса на добавление новой привычке"""
    response = requests.post(API_URL, json=habit)
    if response.status_code == 200:
        return True
    return False


def request_to_get_all_active_habits() -> bool | List[dict]:
    """Получение списка всех активных привычек"""
    response = requests.get(API_URL)
    data = response.json()
    if data is None:
        return False
    return data