import logging
import telegram
import re

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from telega_bot import bot_conf, weather_utils
from telega_bot import openweathermap
from rubik import medicum_registr


def button(update, context):
    query = update.callback_query

    keyboard = None
    reply_markup = None
    text = None

    #  Get region/country/city name between ::, eg. region:Europe:EU
    pattern = r'.*?:(.*):.*'
    match = re.search(pattern, query.data)
    data_name = match.group(1)

    if 'region:' in query.data:
        keyboard = weather_utils.create_countries_keyboard(query.data[-2::1])
        text = "Выбран регион: {}".format(data_name)
    elif 'country:' in query.data:
        keyboard = weather_utils.create_cities_keyboard(query.data[-2::1])
        text = "Выбрана страна: {}".format(data_name)
    elif 'city:' in query.data:
        temperature = openweathermap.get_temp_by_city_id(re.findall(r'\d+', update.callback_query.data)[0])
        text = "{} {}".format(data_name, temperature)

    if keyboard:
        reply_markup = InlineKeyboardMarkup(keyboard)

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
            temp = openweathermap.get_temp_by_city_name(text[1])
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
