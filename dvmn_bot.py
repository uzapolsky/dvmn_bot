import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, ReadTimeout


logger = logging.getLogger('Logger')

class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot_log, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot_log = bot_log

    def emit(self, record):
        log_entry = self.format(record)
        self.bot_log.send_message(chat_id=self.chat_id, text=log_entry)


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
    bot_log = telegram.Bot(token=os.environ['BOT_LOG_TOKEN'])
    chat_id = os.environ['CHAT_ID']
    dvmn_token = os.environ['DVMN_TOKEN']
    url = 'https://dvmn.org/api/long_polling/'

    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(bot_log, chat_id))

    headers = {
        'Authorization': f'Token {dvmn_token}',
    }
    
    payload = {}

    while True:
        try:
            try:
                response = requests.get(url, headers=headers, params=payload, timeout=60)
                response.raise_for_status()
            except ReadTimeout:
                continue
            except ConnectionError:
                logger.warning('Проблемы с интернетом')
                time.sleep(30)
                continue

            answer = response.json()
            if answer['status'] == 'timeout':
                payload['timestamp'] = answer['timestamp_to_request']
            if answer['status'] == 'found':
                payload['timestamp'] = answer['last_attempt_timestamp']
                send_message(answer, bot, chat_id)
        except telegram.error.TelegramError:
            logger.exception('Проблема с телеграммом')


if __name__ == '__main__':
    main()
