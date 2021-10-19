import requests
import os
from dotenv import load_dotenv
from requests.exceptions import ReadTimeout, ConnectionError
import time


def main():
    load_dotenv()
    dvmn_token = os.environ['DVMN_TOKEN']
    url = 'https://dvmn.org/api/long_polling/'

    headers = {
        'Authorization': f'Token {dvmn_token}',
    }
    
    response = requests.get(url, headers=headers, timeout=1)
    answer = response.json()
    payload = {
        'timestamp': answer['last_attempt_timestamp'],
    }

    while True:
        try:
            response = requests.get(url, headers=headers, params=payload, timeout=5)
        except ReadTimeout:
            print('Время вышло')
        except ConnectionError:
            print('Подключение к интернету нестабильно')
            time.sleep(1)
        else:
            answer = response.json()
            if answer['status'] == 'timeout':
                payload['timestamp'] = answer['timestamp_to_request']
            if answer['status'] == 'found':
                print(answer)

if __name__ == '__main__':
    main()