from loader import bot
from telebot.types import Message


@bot.message_handler(state=None)
def bot_echo(message: Message):
    bot.reply_to(message, "Для запуска бота, нажмите /start")
