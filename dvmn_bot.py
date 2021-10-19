import requests
import os
from dotenv import load_dotenv
from requests.exceptions import ReadTimeout, ConnectionError
import time
import telegram


def send_message(answer, bot, chat_id):

    for attempt in answer['new_attempts']:
        msg = f'Урок <{attempt["lesson_title"]}> проверен!\n'
        if attempt['is_negative']:
            msg += 'Надо исправить ошибки\n'
        else:
            msg += 'Можно приступать к следующему уроку\n'
        msg += f'Ссылка на урок: {attempt["lesson_url"]}'

    bot.send_message(text=msg, chat_id=chat_id)


def main():
    load_dotenv()

    bot = telegram.Bot(token=os.environ['BOT_TOKEN'])
    chat_id = os.environ['CHAT_ID']
    dvmn_token = os.environ['DVMN_TOKEN']
    url = 'https://dvmn.org/api/long_polling/'

    headers = {
        'Authorization': f'Token {dvmn_token}',
    }
    
    payload = {}

    while True:
        try:
            response = requests.get(url, headers=headers, params=payload, timeout=60)
        except ReadTimeout:
            continue
        except ConnectionError:
            time.sleep(30)
            continue

        answer = response.json()
        if answer['status'] == 'timeout':
            payload['timestamp'] = answer['timestamp_to_request']
        if answer['status'] == 'found':
            send_message(answer, bot, chat_id)


if __name__ == '__main__':
    main()