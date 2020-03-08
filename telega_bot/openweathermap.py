import requests
import pprint

from telega_bot import bot_conf

API_KEY = bot_conf.OPENWEATHERMAP_API_KEY
URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"
URL_BY_CITY_ID = "http://api.openweathermap.org/data/2.5/weather?id={}&units=metric&appid={}"


def get_temp_by_city_name(city):
    resp = requests.get(URL.format(city, API_KEY))
    if resp.status_code == 200:
        temp = resp.json()['main']['temp']
    else:
        temp = 'NaN'
    return temp


def get_temp_by_city_id(city_id):
    resp = requests.get(URL_BY_CITY_ID.format(city_id, API_KEY))
    if resp.status_code == 200:
        temp = resp.json()['main']['temp']
    else:
        temp = 'NaN'
    return temp


if __name__ == '__main__':
    city = "New York City"
    r = get_temp_by_city_name(city)
    print(r)

    # resp = requests.get(URL.format(city, API_KEY)).json()
    # print(resp)

    r = requests.get(URL_BY_CITY_ID.format(591260, API_KEY))
    pprint.pprint(r.json())