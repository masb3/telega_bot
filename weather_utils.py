import requests
import pprint
import json


from telegram import InlineKeyboardButton
from telega_bot import geonames_conf


regions_dict = {'Europe': 'EU', 'Americas': 'NA', 'Asia': 'AS', 'Africa': 'AF', 'Oceania': 'OC'}  # TODO: check others


def dict_by_api_param(param_val, param_name):
    if param_name == 'cities':
        url = 'http://api.geonames.org/searchJSON?country={}&cities=cities15000&username={}'. \
            format(param_val, geonames_conf.API_TOKEN)
        key1_in_resp = 'name'
        key2_in_resp = 'geonameId'
    elif param_name == 'countries':
        url = "http://api.geonames.org/searchJSON?continentCode={}&username={}". \
            format(param_val, geonames_conf.API_TOKEN)
        key1_in_resp = 'countryName'
        key2_in_resp = 'countryCode'
    else:
        url = None
        key1_in_resp = None
        key2_in_resp = None

    ret_dict = {}
    if url:
        response = requests.request("GET", url)

        for resp in response.json()['geonames'][1:]:
            ret_dict.setdefault(resp[key1_in_resp], resp[key2_in_resp])

    return ret_dict


def create_keyboard(data_list, callback_data=None, buttons_in_row=2):
    i = 0
    keyboard = [[]]

    if callback_data == 'country' or callback_data == 'city' or callback_data == 'region':
        for k in data_list.keys():
            if len(keyboard[i]) == buttons_in_row:
                i += 1
                keyboard.append([])

            cb = callback_data + ':' + k + ':' + str(data_list[k])

            keyboard[i].append(InlineKeyboardButton(k, callback_data=cb))

    return keyboard


def create_regions_keyboard():
    return create_keyboard(regions_dict, callback_data='region')


def create_countries_keyboard(region):
    return create_keyboard(dict_by_api_param(region, 'countries'), callback_data='country')


def create_cities_keyboard(country):
    return create_keyboard(dict_by_api_param(country, 'cities'), callback_data='city', buttons_in_row=3)
