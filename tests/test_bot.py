import pytest
import requests
import bot     

MOCK_UPDATE_SINGLE = {
    'message': {
        'chat': {
            'id': 12345
        },
        'text': 'hello'
    }
}

MOCK_UPDATES_LIST = {
    'ok': True,
    'result': [
        {
            'update_id': 101,
            'message': {'chat': {'id': 111}, 'text': 'first message'}
        },
        {
            'update_id': 102,
            'message': {'chat': {'id': 222}, 'text': 'second message'}
        }
    ]
}


def test_get_chat_id():
    """
    Проверяем, что функция get_chat_id правильно извлекает id чата.
    """
    mock_update = MOCK_UPDATE_SINGLE
    
    chat_id = bot.get_chat_id(mock_update)
    
    assert chat_id == 12345

def test_get_message_text():
    """
    Проверяем, что функция get_message_text правильно извлекает текст сообщения.
    """
    mock_update = MOCK_UPDATE_SINGLE
    
    message_text = bot.get_message_text(mock_update)
    
    assert message_text == 'hello'


def test_last_update(mocker):
    """
    Проверяем, что функция last_update:
    1. Вызывает requests.get с правильным URL.
    2. Правильно парсит JSON.
    3. Возвращает ПОСЛЕДНЕЕ обновление из списка.
    """
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = MOCK_UPDATES_LIST
    
    mocker.patch('requests.get', return_value=mock_response)
    
    test_url = "http://fake.url/"
    last_update_result = bot.last_update(test_url)
    
    requests.get.assert_called_once_with(test_url + 'getUpdates')
    
    assert last_update_result['update_id'] == 102
    assert last_update_result['message']['text'] == 'second message'

def test_send_message(mocker):
    """
    Проверяем, что функция send_message:
    1. Вызывает requests.post с правильным URL и данными.
    """

    mock_post = mocker.patch('requests.post')
    
    mocker.patch.object(bot, 'url', 'https://api.telegram.org/botFAKE_TOKEN/')
    
    test_chat_id = 98765
    test_text = "Hello from test!"
    
    bot.send_message(test_chat_id, test_text)
    
    expected_url = 'https://api.telegram.org/botFAKE_TOKEN/sendMessage'
    expected_data = {'chat_id': test_chat_id, 'text': test_text}
    
    mock_post.assert_called_once_with(expected_url, data=expected_data)
    