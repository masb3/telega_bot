from telega_bot.telega_bot_requests import BotHandler
from telega_bot import bot_conf

if __name__ == '__main__':
    bot = BotHandler(token=bot_conf.TOKEN, poll_period_s=1)
    # try:
    #     bot.polling()
    # except KeyboardInterrupt:
    #     exit()