from telebot.types import Message

from main import bot


@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.full_name}! Это Бот.\nЯ умею отслеживать выполнение твоих привычек.")
