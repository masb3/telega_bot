import requests
import pprint
import datetime

from telega_bot import bot_conf

API_KEY = bot_conf.OPENWEATHERMAP_API_KEY
URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"
URL_BY_CITY_ID = "http://api.openweathermap.org/data/2.5/weather?id={}&units=metric&appid={}"
URL_TOMORROW_BY_CITY_ID = "http://api.openweathermap.org/data/2.5/forecast?id={}&units=metric&appid={}"

# Openweathermap Weather codes and corressponding emojis
thunderstorm = u'\U0001F4A8'  # Code: 200's, 900, 901, 902, 905
drizzle = u'\U0001F4A7'  # Code: 300's
rain = u'\U00002614'  # Code: 500's
snowflake = u'\U00002744'  # Code: 600's snowflake
snowman = u'\U000026C4'  # Code: 600's snowman, 903, 906
atmosphere = u'\U0001F301'  # Code: 700's foogy
clear_sky = u'\U00002600'  # Code: 800 clear sky
few_clouds = u'\U000026C5'  # Code: 801 sun behind clouds
clouds = u'\U00002601'  # Code: 802-803-804 clouds general
hot = u'\U0001F525'  # Code: 904
default_emoji = u'\U0001F300'  # default emojis


def get_emoji(weather_id):
    if weather_id:
        if str(weather_id)[0] == '2' or weather_id == 900 or weather_id == 901 or weather_id == 902 or weather_id == 905:
            return thunderstorm
        elif str(weather_id)[0] == '3':
            return drizzle
        elif str(weather_id)[0] == '5':
            return rain
        elif str(weather_id)[0] == '6' or weather_id == 903 or weather_id == 906:
            return snowflake + ' ' + snowman
        elif str(weather_id)[0] == '7':
            return atmosphere
        elif weather_id == 800:
            return clear_sky
        elif weather_id == 801:
            return few_clouds
        elif weather_id == 802 or weather_id == 803 or weather_id == 804:
            return clouds
        elif weather_id == 904:
            return hot
        else:
            return default_emoji  # Default emoji

    else:
        return default_emoji  # Default emoji


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
        feels_like = resp.json()['main']['feels_like']
        wind = resp.json()['wind']['speed']
        main = resp.json()['weather'][0]['description'][0].upper() + resp.json()['weather'][0]['description'][1:] \
               + ' ' + get_emoji(resp.json()['weather'][0]['id'])

    else:
        temp = 'NaN'
        feels_like = 'NaN'
        wind = 'NaN'
        main = 'NaN'
    return temp, feels_like, wind, main


def get_temp_tomorrow_by_city_id(city_id):
    resp = requests.get(URL_TOMORROW_BY_CITY_ID.format(city_id, API_KEY))
    if resp.status_code == 200:
        text = "{}\n".format(resp.json()['city']['name'])
        for i in range(3, 8, 2):
            dt = datetime.datetime.utcfromtimestamp(resp.json()['list'][i]['dt']).strftime('%m.%d %H:%M')
            temp = resp.json()['list'][i]['main']['temp']
            feels_like = resp.json()['list'][i]['main']['feels_like']
            wind = resp.json()['list'][i]['wind']['speed']
            main = resp.json()['list'][i]['weather'][0]['description'][0].upper() + \
                   resp.json()['list'][i]['weather'][0]['description'][1:] \
                   + ' ' + get_emoji(resp.json()['list'][i]['weather'][0]['id'])

            text += "{}\n\U0001F321 {}\nFeels like: {}\nWind: {} m/s\n{}\n\n".\
                format(dt, temp, feels_like, wind, main)
    else:
        text = 'NaN'
    return text


if __name__ == '__main__':
    city = "New York City"
    r = get_temp_by_city_name(city)
    print(r)

    # resp = requests.get(URL.format(city, API_KEY)).json()
    # print(resp)

    r = requests.get(URL_BY_CITY_ID.format(591260, API_KEY))
    pprint.pprint(r.json())
