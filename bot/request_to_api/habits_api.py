from typing import Dict, List, Optional, Any

import requests

API_URL = "http://127.0.0.1:8000/api/habits"  # Адрес FastAPI


def request_to_new_habit(habit: Dict) -> bool:
    """
    Отправка запроса на добавление новой привычке
    :param habit: dict - Словарь с данными о новой привычке
    :return: True если привычка добавлена, в противном случае False.
    """
    response = requests.post(API_URL, json=habit)
    if response.status_code == 200:
        return True
    return False


def request_to_get_all_active_habits() -> bool | List[dict]:
    """
    Получение списка всех активных привычек
    :return: Список с привычками
    """
    response = requests.get(API_URL)
    data = response.json()
    if data is None:
        return False
    return data


def request_to_get_habit_by_id(habit_id: int) -> bool | Any:
    """
    Получение привычки по id
    :param habit_id: int - id привычки
    :return: модель Habit
    """
    response = requests.get(API_URL + f"/{habit_id}")
    data = response.json()
    if data is None:
        return False
    return data
