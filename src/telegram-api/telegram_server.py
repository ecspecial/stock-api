import os
import time
import requests
from dotenv import load_dotenv

# Загрузка переменных среды из файла .env
load_dotenv()

# Получение токена бота Telegram из переменной среды
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Получение идентификатора чата из переменной среды
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Функция для отправки уведомления об ошибке в Telegram
def send_error_notification():
    try:
        # Конечная точка API бота Telegram для отправки сообщений
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        # Параметры для сообщения
        params = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": "❌ Сервер не отвечает ❌"
        }

        # Отправка POST-запроса к API бота Telegram
        response = requests.post(url, params=params)

        # Проверка успешности запроса
        if response.ok:
            print("Уведомление об ошибке успешно отправлено.")
        else:
            print("Не удалось отправить уведомление об ошибке.")
    except requests.RequestException as e:
        print("Ошибка при отправке уведомления:", e)

# Функция для отправки запроса на тестовый эндпоинт сервера
def send_test_request():
    try:
        # Отправка GET-запроса на тестовый эндпоинт
        response = requests.get('http://localhost:5000/test')
        
        # Проверка статуса ответа
        if response.status_code == 200:
            # Если ответ от сервера успешный, возвращаем True
            return True
        else:
            # Если ответ от сервера неуспешный, возвращаем False
            return False
    except requests.RequestException as e:
        # Если произошла ошибка при отправке запроса, возвращаем False
        print('Ошибка при отправке запроса:', e)
        return False

# Основная функция для проверки статуса работы сервера
def check_server_status():
    # Переменная для отслеживания количества попыток отправки запроса
    attempts = 0
    
    while True:
        # Отправка запроса на тестовый эндпоинт
        success = send_test_request()
        
        if success:
            # Если получен успешный ответ, выводим сообщение о работе сервера
            # print('Сервер работает')
            # Переход к следующей итерации через 5 минут
            time.sleep(300)
        else:
            # Если получен неуспешный ответ, увеличиваем счетчик попыток
            attempts += 1
            if attempts == 3:
                # Если количество попыток достигло 3, отправляем уведомление об ошибке
                send_error_notification()
                # Сброс счетчика попыток
                attempts = 0
            else:
                # Если количество попыток меньше 3, ждем 1 минуту перед следующей попыткой
                time.sleep(60)

# Вызов функции для проверки статуса работы сервера
check_server_status()