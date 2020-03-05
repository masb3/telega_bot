import requests
import pprint
import json


from telegram import InlineKeyboardButton
from telega_bot import geonames_conf


regions_list = ['Europe', 'Americas', 'Asia', 'Africa', 'Oceania']
regions_dict = {'Europe': 'EU', 'Americas': 'NA', 'Asia': 'AS', 'Africa': 'AF', 'Oceania': 'OC'}  # TODO: check others


def list_of_countries_by_region(region):
    url = "http://api.geonames.org/searchJSON?continentCode={}&username={}".\
        format(regions_dict[region], geonames_conf.API_TOKEN)
    response = requests.request("GET", url)

    countries_d = {}
    for resp in response.json()['geonames'][1:]:
        countries_d.setdefault(resp['countryName'], resp['countryCode'])
    return countries_d


def list_of_cities_by_country(country):
    url = 'http://api.geonames.org/searchJSON?country={}&cities=cities15000&username={}'.\
        format(country, geonames_conf.API_TOKEN)
    response = requests.request("GET", url)

    cities_d = {}
    for resp in response.json()['geonames'][1:]:
        cities_d.setdefault(resp['name'], resp['geonameId'])

    return cities_d


def create_keyboard(data_list, callback_data=None, buttons_in_row=2):
    i = 0
    keyboard = [[]]

    if callback_data == 'country' or callback_data == 'city':
        for k in data_list.keys():
            if len(keyboard[i]) == buttons_in_row:
                i += 1
                keyboard.append([])

            cb = callback_data + ':' + k + ':' + str(data_list[k])

            keyboard[i].append(InlineKeyboardButton(k, callback_data=cb))
        return keyboard

    else:
        for data in data_list:
            if len(keyboard[i]) == buttons_in_row:
                i += 1
                keyboard.append([])

            cb = data

            keyboard[i].append(InlineKeyboardButton(data, callback_data=cb))
        return keyboard


def create_regions_keyboard():
    return create_keyboard(regions_list)


def create_countries_keyboard(region):
    return create_keyboard(list_of_countries_by_region(region), callback_data='country')


def create_cities_keyboard(country):
    return create_keyboard(list_of_cities_by_country(country), callback_data='city', buttons_in_row=3)