import requests
import pprint
import threading

from time import sleep
from telega_bot.openweathermap import openweathermap
from telega_bot.rubik import medicum_registr


class BotHandler:
    def __init__(self, token, poll_period_s, offset=1, timeout=10):
        self.url = "https://api.telegram.org/bot{}/".format(token)
        self.updates = []
        self.poll_period = poll_period_s
        self.offset = offset
        self.timeout = timeout
        self.update_id = None
        self.last_replied_update_id = None

        self.polling_thread = threading.Thread(target=self.polling)
        self.polling_thread_stop = threading.Event()
        self.polling_thread_stop.clear()
        self.start_bot()

    def get_updates(self):
        method = 'getUpdates'
        update_id = self.last_update(content_type='update_id')
        if update_id is None:
            update_id = 0
        querystring = {'offset': update_id + self.offset, 'timeout': self.timeout}
        resp = requests.get(self.url + method, data=querystring)
        if resp.status_code == 200 and resp.json()['ok'] is True:
            self.updates = resp.json()['result']
            if len(self.updates) > 0:
                self.update_id = self.updates[-1]['update_id']
                self.handle_incoming_object()
        else:
            print('====== {} ERROR code = {}'.format(self.get_updates.__name__, resp.status_code))

    def get_object(self):
        obj = None
        obj_type = None
        try:
            obj = self.updates[-1]
        except IndexError:  # In case bot restarted
            pass
        else:
            list_of_keys = ['message', 'callback_query']
            for k in list_of_keys:
                if k in obj.keys():
                    obj = obj.get(k)
                    obj_type = k
                    break

        return obj, obj_type

    def last_update(self, content_type=None):
        try:
            ret = self.updates[-1]
            print(ret)
        except IndexError:  # In case bot restarted
            ret = None
        else:
            if content_type:
                if content_type.lower() == 'updates':
                    pass
                elif content_type.lower() == 'update_id':
                    ret = self.update_id
                elif content_type.lower() == 'message':
                    ret = ret['message']
                elif content_type.lower() == 'text':
                    ret = ret['message']['text']
                elif content_type.lower() == 'chat_id':
                    ret = ret['message']['chat']['id']
                elif content_type.lower() == 'message_id':
                    ret = ret['message']['message_id']
                else:
                    print('====== {} ERROR unknown content_type'.format(self.last_update.__name__))
        return ret

    def send_message_text(self, text, chat_id, reply_to_message_id=None, reply_markup=None):
        method = 'sendMessage'
        querystring = {'chat_id': chat_id, 'text': text}
        if reply_to_message_id:
            querystring.update(reply_to_message_id=reply_to_message_id)
        if reply_markup:
            querystring.update(reply_markup=reply_markup)

        resp = requests.post(self.url + method, data=querystring)
        if resp.status_code != 200:
            print('====== {} ERROR code = {}'.format(self.send_message_text.__name__, resp.status_code))

    def reply_message(self, reply_text, chat_id, message_id, reply_markup=None):
        self.send_message_text(reply_text, chat_id, message_id, reply_markup)

    def bot_command(self, cmd):
        repl_txt = ''
        reply_markup = None
        if len(cmd) >= 2 and (cmd[0] == 'temp' or cmd[0] == 'темп'):
            repl_txt = str(openweathermap.get_temp(" ".join(cmd[1:])))
        elif cmd[0] == '/temp':
            repl_txt = 'some text'
            reply_markup = '{"inline_keyboard": [[{"text": "button 1", "callback_data": "service1"}, {"text": "button 2", "callback_data": "service2"}]]}'

        elif cmd[0] == '/rubik':
            resp = medicum_registr.get_free_rubik()
            resp.insert(0, "total = {}".format(len(resp)))
            repl_txt = "\n".join(resp)

        if len(repl_txt) > 0:
            self.reply_message(repl_txt,
                               self.last_update(content_type='chat_id'),
                               self.last_update(content_type='message_id',),
                               reply_markup=reply_markup)

    def parse_text(self, text):
        repl_txt = ''
        list_of_cmds = ['/rubik', '/temp', '/menu']
        if text[0] in list_of_cmds:
            self.bot_command(text)

        elif len(text) >= 2 and (text[0] == 'temp' or text[0] == 'темп'):
            repl_txt = str(openweathermap.get_temp(" ".join(text[1:])))

        elif text[0] == 'rubik':
            resp = medicum_registr.get_free_rubik()
            resp.insert(0, "total = {}".format(len(resp)))
            repl_txt = "\n".join(resp)

        if len(repl_txt) > 0:
            self.reply_message(repl_txt,
                               self.last_update(content_type='chat_id'),
                               self.last_update(content_type='message_id'))

    def handle_incoming_object(self):
        if self.last_replied_update_id is None or self.last_replied_update_id < self.update_id:
            self.last_replied_update_id = self.update_id

            obj, obj_type = self.get_object()
            if obj:
                if 'message' == obj_type:
                    text = self.last_update(content_type='text').lower().split()
                    self.parse_text(text)
                elif 'callback_query' == obj_type:
                    print('******** here')
                    print(obj)

                    self.reply_message("callback",
                                       obj['message']['chat']['id'],
                                       obj['message']['message_id'],
                                       reply_markup=None)

                else:
                    raise NotImplemented

    def start_bot(self):
        self.polling_thread.start()

    def stop_bot(self):
        self.polling_thread_stop.set()

    def polling(self):
        while not self.polling_thread_stop.is_set():
            sleep(self.poll_period)
            self.get_updates()

            pprint.pprint(self.updates)
            print(len(self.updates))
            print('==========================================')


if __name__ == '__main__':
    pass
