from telebot.custom_filters import StateFilter

from loader import bot
from utils.set_bot_commands import set_default_commands
import handlers

if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.polling(2)


