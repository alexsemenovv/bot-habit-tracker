import telebot

from config_data import config


token = config.BOT_TOKEN
bot = telebot.TeleBot(token)

