import time
import requests
import random
import os
from dotenv import load_dotenv
from commands.calculator import calculate_expression
from commands.weather import get_weather

load_dotenv()

bot_key = os.getenv("TOKEN")
URL = os.getenv("URL")
url = f"{URL}{bot_key}/" 

class Bot:
    COMMANDS = {'hi', 'hello', 'hey',
                'csc31',
                'gin',
                'python',
                'dice',
                'weather'}

    def __init__(self, token, url):
        self.token = token
        self.url = url
        self.update = None

    def _last_update(self, request):
        response = requests.get(request + 'getUpdates')
        response = response.json()
        
        if 'result' in response and len(response['result']) > 0:
            results = response['result']
            total_updates = len(results) - 1
            return results[total_updates]
        return None

    def _get_chat_id(self, update):
        chat_id = update['message']['chat']['id']
        return chat_id

    def _get_message_text(self, update):
        if 'text' in update['message']:
            return update['message']['text']
        return ""

    def _send_message(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(self.url + 'sendMessage', data=params)
        return response


    def _handle_greeting(self, update):
        chat_id = self._get_chat_id(update)
        self._send_message(chat_id, 'Greetings! Type "Dice" to roll the dice!')

    def _handle_csc31(self, update):
        chat_id = self._get_chat_id(update)
        message_text = 'Python'
        self._send_message(chat_id, message_text)

    def _handle_gin(self, update):
        chat_id = self._get_chat_id(update)
        self._send_message(chat_id, 'Finish')

    def _handle_python(self, update):
        chat_id = self._get_chat_id(update)
        self._send_message(chat_id, 'version 3.10')

    def _handle_dice(self, update):
        chat_id = self._get_chat_id(update)
        val_1 = random.randint(1, 6)
        val_2 = random.randint(1, 6)
        msg = f'You have {val_1} and {val_2}!\nYour result is {val_1 + val_2}!'
        self._send_message(chat_id, msg)

    def _handle_weather(self, update):
        chat_id = self._get_chat_id(update)
        text = self._get_message_text(update).lower()
        city = text.replace('weather', '').strip()
        
        if not city:
            self._send_message(chat_id, "Please specify a city. Example: weather London")
            return

        weather_info = get_weather(city)
        self._send_message(chat_id, weather_info)

    def _handle_default(self, update):
        chat_id = self._get_chat_id(update)
        text = self._get_message_text(update)
        
        result = calculate_expression(text)
        if result is not None:
            self._send_message(chat_id, result)
        else:
            self._send_message(chat_id, 'Sorry, I don\'t understand you :(')


    def run(self):
        last_update = self._last_update(self.url)
        update_id = last_update['update_id'] if last_update else 0

        print("Bot started...")

        try:
            while True:
                time.sleep(1)
                self.update = self._last_update(self.url)

                if self.update is None or self.update['update_id'] == update_id:
                    continue
                
                update_id = self.update['update_id']
                
                message_text = self._get_message_text(self.update).lower()
                
                if message_text in ['hi', 'hello', 'hey']:
                    self._handle_greeting(self.update)

                elif message_text == 'csc31':
                    self._handle_csc31(self.update)

                elif message_text == 'gin':
                    self._handle_gin(self.update)
                    break

                elif message_text == 'python':
                    self._handle_python(self.update)

                elif message_text == 'dice':
                    self._handle_dice(self.update)

                elif 'weather' in message_text:
                    self._handle_weather(self.update)

                else:
                    self._handle_default(self.update)

        except KeyboardInterrupt:
            print('\nBot has been stopped')
        except Exception as e:
            print(f'\nError occured: {e}')

if __name__ == '__main__':
    bot = Bot(bot_key, url)
    bot.run()