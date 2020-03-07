import telebot

from telega_bot.bot_conf import *



bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'zavod' or message.text.lower() == 'завод':
        text = 'сила'
    else:
        text = 'echo'
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':

    bot.polling()