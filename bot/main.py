import os
import telebot


token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)

