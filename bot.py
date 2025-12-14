import os
import random
import string
import time
from datetime import datetime

import requests
from dotenv import load_dotenv

from commands.calculator import calculate_expression
from commands.weather import get_weather

load_dotenv()

bot_key = os.getenv("TOKEN")
URL = os.getenv("URL", "")
url = f"{URL}{bot_key}/"

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Bot(metaclass=Singleton):
    COMMANDS = {'hi', 'hello', 'hey',
                'csc31', 'gin', 'python',
                'dice', 'weather',
                'coin', 'pass', 'time', 'fact', 'upper', 'help'}

    def __init__(self, token, url):
        self.token = token
        self.url = url

    def _last_update(self, request):
        try:
            response = requests.get(request + 'getUpdates')
            response = response.json()
            
            if 'result' not in response or not response['result']:
                return None
            
            results = response['result']
            total_updates = len(results) - 1
            return results[total_updates]
        except Exception as e:
            print(f"Error getting updates: {e}")
            return None

    def _get_chat_id(self, update):
        chat_id = update['message']['chat']['id']
        return chat_id

    def _get_message_text(self, update):
        if 'message' in update and 'text' in update['message']:
            return update['message']['text']
        return ""

    def _send_message(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(self.url + 'sendMessage', data=params)
        return response

    def _handle_csc31(self, update):
        chat_id = self._get_chat_id(update)
        message_text = 'Python'
        return self._send_message(chat_id, message_text)

    def _generate_password(self, length=12):
        characters = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(random.choice(characters) for i in range(length))

    def _get_random_fact(self):
        facts = [
            "Пингвины делают предложения своим избранницам, вручая камушек.",
            "Мед никогда не портится. Археологи находили съедобный мед в древних египетских гробницах.",
            "Октопусы имеют три сердца.",
            "Бананы являются ягодами, а клубника — нет.",
            "В Шотландии национальное животное — единорог."
        ]
        return random.choice(facts)

    def run(self):
        print("Бот запущен...")
        bot_work = True
        last_update_id = None
        
        while bot_work:
            try:
                last_update = self._last_update(self.url)
                
                if last_update is None:
                    time.sleep(2)
                    continue

                update_id = last_update['update_id']
                
                if last_update_id != update_id:
                    last_update_id = update_id
                    
                    self.update = last_update
                    text = self._get_message_text(self.update).lower()
                    chat_id = self._get_chat_id(self.update)
                    
                    print(f"Получено сообщение: {text}")

                    if text in ['hi', 'hello', 'hey']:
                        self._send_message(chat_id, 'Greetings! Type "help" to see commands!')

                    elif text == 'help':
                        help_text = (
                            "Available commands:\n"
                            "dice - Roll dice\n"
                            "coin - Flip a coin\n"
                            "pass - Generate password\n"
                            "time - Current time\n"
                            "fact - Random fact\n"
                            "weather - Get weather\n"
                            "upper <text> - Make text uppercase\n"
                            "gin - Stop bot"
                        )
                        self._send_message(chat_id, help_text)

                    elif text == 'csc31':
                        self._handle_csc31(self.update)

                    elif text == 'gin':
                        self._send_message(chat_id, 'Finish. Bye!')
                        bot_work = False

                    elif text == 'python':
                        self._send_message(chat_id, 'version 3.10')

                    elif 'weather' in text:
                        city = text.replace('weather', '').strip()
                        if city:
                            weather = get_weather(city)
                            self._send_message(chat_id, weather)
                        else:
                            self._send_message(chat_id, "Please specify a city. Example: weather London")

                    elif text == 'dice':
                        _1 = random.randint(1, 6)
                        _2 = random.randint(1, 6)
                        self._send_message(chat_id, f'You have {_1} and {_2}!\nYour result is {_1 + _2}!')

                    elif text == 'coin':
                        result = random.choice(['Heads (Орел)', 'Tails (Решка)'])
                        self._send_message(chat_id, f'Coin flip result: {result}')

                    elif text == 'pass' or text == 'password':
                        pwd = self._generate_password()
                        self._send_message(chat_id, f'Your strong password: {pwd}')

                    elif text == 'time':
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self._send_message(chat_id, f'Server time: {now}')

                    elif text == 'fact':
                        fact = self._get_random_fact()
                        self._send_message(chat_id, fact)

                    elif text.startswith('upper '):
                        msg_to_upper = text.replace('upper ', '').upper()
                        self._send_message(chat_id, msg_to_upper)

                    else:
                        result = calculate_expression(text)
                        if result is not None:
                            self._send_message(chat_id, result)
                        else:
                            self._send_message(chat_id, 'Sorry, I don\'t understand you :( Type "help"')

                time.sleep(1) 

            except KeyboardInterrupt:
                print('\nБот зупинено вручную')
                bot_work = False
            except Exception as e:
                print(f"Critical Error: {e}")
                time.sleep(5)

if __name__ == '__main__':
    bot = Bot(bot_key, url)
    
    bot.run()
