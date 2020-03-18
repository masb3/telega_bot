import requests
import pprint
import json


from telegram import InlineKeyboardButton
from telega_bot import bot_conf


regions_dict = {'Europe': 'EU', 'Americas': 'NA', 'Asia': 'AS', 'Africa': 'AF', 'Oceania': 'OC'}  # TODO: check others

# Cities/Countries cache
cached_cities_api_call = {}
cached_countries_api_call = {}


def dict_by_api_param(param_val, param_name):
    ret_dict = {}

    #  Check if cached values can be used
    if param_name == 'cities' and param_val in cached_cities_api_call.keys():
        ret_dict = cached_cities_api_call[param_val]
    elif param_name == 'countries' and param_val in cached_countries_api_call.keys():
        ret_dict = cached_countries_api_call[param_val]
    else:  # No cache match
        if param_name == 'cities':
            url = 'http://api.geonames.org/searchJSON?country={}&cities=cities15000&username={}'. \
                format(param_val, bot_conf.GEONAMES_API_KEY)
            key1_in_resp = 'name'
            key2_in_resp = 'geonameId'
        elif param_name == 'countries':
            url = "http://api.geonames.org/searchJSON?continentCode={}&username={}". \
                format(param_val, bot_conf.GEONAMES_API_KEY)
            key1_in_resp = 'countryName'
            key2_in_resp = 'countryCode'
        else:
            url = None
            key1_in_resp = None
            key2_in_resp = None

        if url:
            response = requests.request("GET", url)

            for resp in response.json()['geonames'][1:]:
                ret_dict.setdefault(resp[key1_in_resp], resp[key2_in_resp])

            # Manually add Tallinn to list
            if param_val == 'EE':
                ret_dict.setdefault('Tallinn', 862995)  # 588409

        #  Add to cache last API resp
        if param_name == 'cities':
            cached_cities_api_call.setdefault(param_val, ret_dict)
        elif param_name == 'countries':
            cached_countries_api_call.setdefault(param_val, ret_dict)
    return ret_dict


def create_keyboard(data_list, callback_data, buttons_in_row=2):
    i = 0
    keyboard = [[]]

    for k in data_list.keys():
        if len(keyboard[i]) == buttons_in_row:
            i += 1
            keyboard.append([])

        cb = callback_data + ':' + k + ':' + str(data_list[k])

        keyboard[i].append(InlineKeyboardButton(k, callback_data=cb))

    return keyboard


def create_regions_keyboard(is_temp_tomorrow=False):
    if is_temp_tomorrow:
        callback_data = 'region_tomorrow'
    else:
        callback_data = 'region'
    return create_keyboard(regions_dict, callback_data=callback_data)


def create_countries_keyboard(region, is_temp_tomorrow=False):
    if is_temp_tomorrow:
        callback_data = 'country_tomorrow'
    else:
        callback_data = 'country'

    return create_keyboard(dict_by_api_param(region, 'countries'), callback_data=callback_data, buttons_in_row=3)


def create_cities_keyboard(country, is_temp_tomorrow=False):
    if is_temp_tomorrow:
        callback_data = 'city_tomorrow'
    else:
        callback_data = 'city'
    return create_keyboard(dict_by_api_param(country, 'cities'), callback_data=callback_data, buttons_in_row=3)


def create_save_settings_keyboard(temp_tomorrow=False):
    if temp_tomorrow:
        callback_data = 'save_settings_tomorrow'
    else:
        callback_data = 'save_settings'
    return create_keyboard({'YES': 'yes', 'NO': 'no'}, callback_data=callback_data)
