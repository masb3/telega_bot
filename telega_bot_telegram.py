import logging
import telegram

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from telega_bot import bot_conf, weather_utils
from telega_bot.openweathermap import openweathermap
from telega_bot.rubik import medicum_registr


def button(update, context):
    query = update.callback_query

    keyboard = None
    reply_markup = None
    temperature = None

    if query.data in weather_utils.regions_list:
        keyboard = weather_utils.create_countries_keyboard(query.data)
    elif 'country:' in query.data:
        keyboard = weather_utils.create_cities_keyboard(query.data.replace('country:', ''))
    else:
        temperature = openweathermap.get_temp(update.callback_query.data)

    if keyboard:
        text = "Выбран регион: {}".format(query.data)
        reply_markup = InlineKeyboardMarkup(keyboard)
    else:
        text = "{} {}".format(query.data, temperature)

    # context.bot.edit_message_text(chat_id=query.message.chat_id,
    #                               message_id=query.message.message_id,
    #                               text=text,
    #                               reply_markup=reply_markup)

    context.bot.send_message(chat_id=query.message.chat_id,
                             text=text,
                             message_id=query.message.message_id,
                             reply_markup=reply_markup)

    # query.message.reply_text(text, reply_markup=reply_markup)


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
    reply_markup = InlineKeyboardMarkup(weather_utils.create_regions_keyboard())
    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_to_message_id=update.effective_message.message_id,
                             text='Пожалуйста выберите:',
                             reply_markup=reply_markup)

    # reply_markup = telegram.ReplyKeyboardRemove()
    # context.bot.send_message(chat_id=update.effective_chat.id, text="I'm back.", reply_markup=reply_markup)


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

    dispatcher.add_handler(CallbackQueryHandler(button))


if __name__ == '__main__':
    updater = Updater(token=bot_conf.TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    register_all_handlers(dispatcher)

    updater.start_polling()
    updater.idle()
