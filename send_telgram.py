import requests

from get_config import get_config

config = get_config()
token = config['token']
chat_id = config['chat_id']


def send_msg(msg):
    req = requests.post(url=f'https://api.telegram.org/bot{token}/sendMessage',
                        json={'chat_id': chat_id,
                              'text': msg})
    return req.text
