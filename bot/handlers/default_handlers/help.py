from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = ("/new_habit - Добавление новой привычки",)
    bot.reply_to(message, "\n".join(text))
