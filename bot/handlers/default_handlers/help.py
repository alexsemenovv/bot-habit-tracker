from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = (
        "/new_habit - Добавление новой привычки",
        "/list_habits - Получение списка действующих привычек",
    )
    bot.reply_to(message, "\n".join(text))
