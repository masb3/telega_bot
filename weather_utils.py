import requests
import pprint
import json

from telegram import InlineKeyboardButton


regions_list = ['Europe', 'Americas', 'Asia', 'Africa', 'Oceania']


def list_of_countries_by_region(region):
    url = "https://restcountries.eu/rest/v2/region/{}".format(region)
    response = requests.request("GET", url)

    countries = []
    for resp in response.json():
        countries.append(resp['name'])
    return countries


def list_of_cities_by_country(country):
    countries = []
    with open('geo.json') as json_file:
        data = json.load(json_file)
        for p in data[country]:
            countries.append(p)

    return countries


def create_keyboard(data_list, callback_data=None, buttons_in_row=2):
    i = 0
    keyboard = [[]]
    for data in data_list:
        if len(keyboard[i]) == buttons_in_row:
            i += 1
            keyboard.append([])

        if callback_data == 'country':
            cb = callback_data + ':' + data
        else:
            cb = data

        keyboard[i].append(InlineKeyboardButton(data, callback_data=cb))
    return keyboard


def create_regions_keyboard():
    return create_keyboard(regions_list)


def create_countries_keyboard(region):
    return create_keyboard(list_of_countries_by_region(region), callback_data='country')


def create_cities_keyboard(country):
    return create_keyboard(list_of_cities_by_country(country), buttons_in_row=3)