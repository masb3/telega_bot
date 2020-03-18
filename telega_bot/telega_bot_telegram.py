import logging
import telegram
import re
import pprint

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from telega_bot import bot_conf, weather_utils, openweathermap, db_utils
from rubik import medicum_registr


def callback_handler(update, context):
    query = update.callback_query

    keyboard = None
    reply_markup = None
    text = None

    #  Get region/country/city name between ::, eg. region:Europe:EU
    pattern = r'.*?:(.*):.*'
    match = re.search(pattern, query.data)
    data_name = match.group(1)

    if 'region:' in query.data or 'region_tomorrow:' in query.data:
        user_id = db_utils.get_saved_user_id(update.effective_user['id'])
        if user_id is not None:
            db_utils.update_last_region(data_name, query.data[-2::1], user_id)

        if 'region_tomorrow:' in query.data:
            is_temp_tomorrow = True
        else:
            is_temp_tomorrow = False

        keyboard = weather_utils.create_countries_keyboard(query.data[-2::1], is_temp_tomorrow)
        text = "Region selected: {}".format(data_name)

    elif 'country:' in query.data or 'country_tomorrow:' in query.data:
        user_id = db_utils.get_saved_user_id(update.effective_user['id'])
        if user_id is not None:
            db_utils.update_last_country(data_name, query.data[-2::1], user_id)

        if 'country_tomorrow:' in query.data:
            is_temp_tomorrow = True
        else:
            is_temp_tomorrow = False

        keyboard = weather_utils.create_cities_keyboard(query.data[-2::1], is_temp_tomorrow)
        text = "Country selected: {}".format(data_name)

    elif 'city:' in query.data:
        user_id = db_utils.get_saved_user_id(update.effective_user['id'])
        if user_id is not None:
            db_utils.update_last_city(data_name, re.findall(r'\d+', update.callback_query.data)[0], user_id)

        temp, feels_like, wind, main = \
            openweathermap.get_temp_by_city_id(re.findall(r'\d+', update.callback_query.data)[0])
        text = "{} \U0001F321 {}\nFeels like: {}\nWind: {} m/s\n{}".\
            format(data_name, temp, feels_like, wind, main)

    elif 'city_tomorrow:' in query.data:
        user_id = db_utils.get_saved_user_id(update.effective_user['id'])
        if user_id is not None:
            db_utils.update_last_city(data_name, re.findall(r'\d+', update.callback_query.data)[0], user_id)

        text = openweathermap.get_temp_tomorrow_by_city_id(re.findall(r'\d+', update.callback_query.data)[0])

    elif 'save_settings:' in query.data or 'save_settings_tomorrow:' in query.data:
        if 'save_settings_tomorrow:' in query.data:
            is_temp_tomorrow = True
        else:
            is_temp_tomorrow = False
        keyboard = weather_utils.create_regions_keyboard(is_temp_tomorrow)
        text = 'Please select:'

        if 'save_settings:YES:yes' == query.data or 'save_settings_tomorrow:YES:yes' == query.data:
            db_utils.save_user(update)

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
    text = 'Do you want me to remember your choice?'
    reply_markup = InlineKeyboardMarkup(weather_utils.create_save_settings_keyboard())

    if db_utils.get_saved_user_id(update.effective_user['id']) is not None:
        last_city = db_utils.get_last_city(update.effective_user['id'])
        if last_city:
            temp, feels_like, wind, main = \
                openweathermap.get_temp_by_city_id(last_city[1])
            text = "{} \U0001F321 {}\nFeels like: {}\nWind: {} m/s\n{}".\
                format(last_city[0], temp, feels_like, wind, main)
            reply_markup = None

    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_to_message_id=update.effective_message.message_id,
                             text=text,
                             reply_markup=reply_markup)

    # reply_markup = telegram.ReplyKeyboardRemove()
    # context.bot.send_message(chat_id=update.effective_chat.id, text="I'm back.", reply_markup=reply_markup)


def temp_update(update, context):
    db_utils.reset_user_is_set(update.effective_user['id'])
    text = 'Do you want me to remember your choice?'
    reply_markup = InlineKeyboardMarkup(weather_utils.create_save_settings_keyboard())

    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_to_message_id=update.effective_message.message_id,
                             text=text,
                             reply_markup=reply_markup)


def temp_tomorrow(update, context):
    text = 'Do you want me to remember your choice?'
    reply_markup = InlineKeyboardMarkup(weather_utils.create_save_settings_keyboard(temp_tomorrow=True))

    if db_utils.get_saved_user_id(update.effective_user['id']) is not None:
        last_city = db_utils.get_last_city(update.effective_user['id'])
        if last_city:
            text = openweathermap.get_temp_tomorrow_by_city_id(last_city[1])
            reply_markup = None

    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_to_message_id=update.effective_message.message_id,
                             text=text,
                             reply_markup=reply_markup)


def rubik(update, context):
    resp = medicum_registr.get_free_rubik()
    resp.insert(0, "total = {}".format(len(resp)))
    repl_txt = "\n".join(resp)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_to_message_id=update.effective_message.message_id,
                             text=repl_txt)


def register_all_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('temp', temp))
    dispatcher.add_handler(CommandHandler('temp_update', temp_update))
    dispatcher.add_handler(CommandHandler('temp_tomorrow', temp_tomorrow))
    dispatcher.add_handler(CommandHandler('rubik', rubik))
    dispatcher.add_handler(MessageHandler(Filters.text, text_handler))

    dispatcher.add_handler(CallbackQueryHandler(callback_handler))


if __name__ == '__main__':
    updater = Updater(token=bot_conf.TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    register_all_handlers(dispatcher)

    updater.start_polling()
    updater.idle()
