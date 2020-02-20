import requests

from telega_bot.openweathermap import conf

API_KEY = conf.API_KEY
URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"


def get_temp(city):
    resp = requests.get(URL.format(city, API_KEY))
    if resp.status_code == 200:
        temp = resp.json()['main']['temp']
    else:
        temp = 'NaN'
    return temp


if __name__ == '__main__':
    city = "new-york"
    r = get_temp("new-york")
    print(r)

    # resp = requests.get(URL.format(city, API_KEY)).json()
    # print(resp)