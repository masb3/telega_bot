import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from telega_bot import bot_conf
from telega_bot.openweathermap import openweathermap
from telega_bot.rubik import medicum_registr


def text_handler(update, context):
    try:
        text = update.message.text.lower().split(' ')
        if len(text) >= 2 and 'temp' == text[0]:
            temp = openweathermap.get_temp(text[1])
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     reply_to_message_id=update.effective_message.message_id,
                                     text=temp)
    except IndexError:
        pass


def temp(update, context):
    # todo: reply with list of countries
    temp = openweathermap.get_temp('tallinn')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_to_message_id=update.effective_message.message_id,
                             text=temp)


def rubik(update, context):
    resp = medicum_registr.get_free_rubik()
    resp.insert(0, "total = {}".format(len(resp)))
    repl_txt = "\n".join(resp)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_to_message_id=update.effective_message.message_id,
                             text=repl_txt)


def register_all_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('temp', temp))
    dispatcher.add_handler(CommandHandler('rubik', rubik))
    dispatcher.add_handler(MessageHandler(Filters.text, text_handler))


if __name__ == '__main__':
    updater = Updater(token=bot_conf.TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    register_all_handlers(dispatcher)

    updater.start_polling()
    updater.idle()
