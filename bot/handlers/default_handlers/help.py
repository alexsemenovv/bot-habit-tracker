from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = ("Здесь будет выводится справка",)

    bot.reply_to(message, "\n".join(text))
