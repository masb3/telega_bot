import requests
import json
import pprint

from time import sleep

from telega_bot import bot_conf


class BotHandler:
    def __init__(self, token, poll_period_s, offset=1, timeout=10):
        self.url = "https://api.telegram.org/bot{}/".format(token)
        self.updates = {}
        self.poll_period = poll_period_s
        self.offset = offset
        self.timeout = timeout

    def get_updates(self):
        method = 'getUpdates'
        querystring = {'offset': self.last_update_id() + self.offset, 'timeout': self.timeout}
        resp = requests.get(self.url + method, data=querystring)
        if resp.status_code == 200 and resp.json()['ok'] is True:
            self.updates = resp.json()['result']
        else:
            print('====== {} ERROR code = {}'.format(self.get_updates.__name__, resp.status_code))

    def last_update(self):
        try:
            ret = self.updates[-1]
        except IndexError:
            ret = None
        return ret

    def last_update_id(self):
        if len(self.updates) > 0:
            upd_id = self.last_update()['update_id']
        else:
            upd_id = 0
        return upd_id

    def last_message(self):
        if self.last_update() is not None:
            ret = self.last_update()['message']
        else:
            ret = None
        return ret

    def last_message_text(self):
        if self.last_message() is not None:
            ret = self.last_message()['text']
        else:
            ret = None
        return ret

    def send_message_text(self, text):
        try:
            chat_id = self.last_message()['chat']['id']
        except TypeError:
            print('====== {} ERROR updates is empty'.format(self.send_message_text.__name__))
        else:
            method = 'sendMessage'
            querystring = {'chat_id': chat_id, 'text': text}
            resp = requests.post(self.url + method, data=querystring)
            if resp.status_code != 200:
                print('====== {} ERROR code = {}'.format(self.send_message_text.__name__, resp.status_code))

    def polling(self):
        while True:
            sleep(self.poll_period)
            self.get_updates()

            #self.send_message_text('sample text')

            #print(self.last_message_text())
            #pprint.pprint(self.last_update())
            pprint.pprint(self.updates)
            #print(self.last_update_id())
            print(len(self.updates))
            print('==========================================')


if __name__ == '__main__':
    bot = BotHandler(token=bot_conf.TOKEN, poll_period_s=1)
    try:
        bot.polling()
    except KeyboardInterrupt:
        exit()