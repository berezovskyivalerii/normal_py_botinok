import time
import requests
import random
import os
from dotenv import load_dotenv
load_dotenv()
bot_token = os.getenv("TOKEN")

url = f"https://api.telegram.org/bot{bot_token}/" 


def last_update(request):
    response = requests.get(request + 'getUpdates')
    print(response)
    response = response.json()
    print(response)
    results = response['result']
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
    update_id = last_update(url)['update_id']
    while True:
        time.sleep(3)
        update = last_update(url)
        if update_id == update['update_id']:
            if get_message_text(update).lower() == 'hi' or get_message_text(
                    update).lower() == 'hello' or get_message_text(update).lower() == 'hey':
                send_message(get_chat_id(update), 'Greetings! Type "Dice" to roll the dice!')
            elif get_message_text(update).lower() == 'qa24':
                send_message(get_chat_id(update), 'csc31') 
            #
            elif get_message_text(update).lower() == 'cmd1':
                send_message(get_chat_id(update), 'resp1') 
            elif get_message_text(update).lower() == 'cmd2':
                send_message(get_chat_id(update), 'resp2') 
            elif get_message_text(update).lower() == 'cmd3':
                send_message(get_chat_id(update), 'resp3') 
            #
            elif get_message_text(update).lower() == 'python':
                send_message(get_chat_id(update), 'version 3.14')
            elif get_message_text(update).lower() == 'dice':
                _1 = random.randint(1, 6)
                _2 = random.randint(1, 6)
                send_message(get_chat_id(update),
                             'You have ' + str(_1) + ' and ' + str(_2) + '!\nYour result is ' + str(_1 + _2) + '!')
            else:
                send_message(get_chat_id(update), 'Sorry, I don\'t understand you :(')
            update_id += 1


if __name__ == '__main__':
    main()
