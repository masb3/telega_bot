from time import sleep
from telega_bot.telega_bot_requests import BotHandler
from telega_bot import bot_conf

if __name__ == '__main__':
    bot = BotHandler(token=bot_conf.TELEGRAM_TOKEN, poll_period_s=1)
    try:
        while True:
            sleep(2)
            print('main')
    except KeyboardInterrupt:
        bot.stop_bot()
        exit()

