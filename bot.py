import time
import os
import requests
import random
import datetime
from dotenv import load_dotenv
from calculator import calculate_expression

load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
URL = os.getenv("URL")

url = f"{URL}{TOKEN}/"


def last_update(request):
    response = requests.get(request + 'getUpdates')
    response_json = response.json()
    if not response_json.get('ok', True):
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response_json}")
        import sys
        sys.exit(1)

    results = response_json['result']
    total_updates = len(results) - 1
    return results[total_updates]


def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id


def get_message_text(update):
    message_text = update['message']['text']
    return message_text


def send_message(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response


def main():
    try:
        update_id = last_update(url)['update_id']
        while True:
            time.sleep(3)
            update = last_update(url)
            if update_id == update['update_id']:
                if get_message_text(update).lower() == 'hi' or get_message_text(
                        update).lower() == 'hello' or get_message_text(update).lower() == 'hey':
                    send_message(get_chat_id(update), 'Greetings! Type "Dice" to roll the dice!')
                elif get_message_text(update).lower() == 'qa24':
                    send_message(get_chat_id(update), 'Python')
                elif get_message_text(update).lower() == 'gin':
                    send_message(get_chat_id(update), 'Finish')
                    break
                elif get_message_text(update).lower() == 'python':
                    send_message(get_chat_id(update), 'version 3.10')
                elif get_message_text(update).lower() == 'reverse':
                    reversed_text = get_message_text(update)[::-1] 
                    send_message(get_chat_id(update), reversed_text)
                elif get_message_text(update).lower() == 'id':
                        chat_id = get_chat_id(update)
                        send_message(chat_id, f"Your сhat ID is: {chat_id}")
                elif get_message_text(update).lower() == 'time':
                        now = datetime.datetime.now()
                        current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
                        send_message(get_chat_id(update), f"Current time: {current_time_str}")
                elif get_message_text(update).lower() == 'dice':
                    _1 = random.randint(1, 6)
                    _2 = random.randint(1, 6)
                    send_message(get_chat_id(update),
                                 'You have ' + str(_1) + ' and ' + str(_2) + '!\nYour result is ' + str(_1 + _2) + '!')
                else:
                    result = calculate_expression(get_message_text(update))
                    if result is not None:
                        send_message(get_chat_id(update), result)
                    else:
                        send_message(get_chat_id(update), 'Sorry, I don\'t understand you :(')
                update_id += 1
    except KeyboardInterrupt:
        print('\nБот зупинено')


if __name__ == '__main__':
    main()
