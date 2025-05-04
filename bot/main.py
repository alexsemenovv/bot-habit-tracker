import asyncio
import datetime
import time

import handlers
from loader import bot
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands

if __name__ == "__main__":
    while True:
        try:
            bot.add_custom_filter(StateFilter(bot))
            set_default_commands(bot)
            asyncio.run(bot.polling(non_stop=True, interval=1, timeout=0))
        except Exception as e:
            print(datetime.datetime.now(), e)
            time.sleep(5)
