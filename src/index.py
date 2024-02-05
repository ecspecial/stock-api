import os
import pyodbc
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение строки подключения к базе данных из переменной окружения
DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')

app = Flask(__name__)

# Инициализируем эндпоинт для получения данных по артикулу
@app.route('/get_article', methods=['POST'])
def get_article():
    # Получение данных из JSON-запроса
    data = request.json
    article = data.get('article')
    login = data.get('login')
    password = data.get('password')

    # Подключение к базе данных
    conn = pyodbc.connect(DB_CONNECTION_STRING)
    cursor = conn.cursor()

    # Проверка учетных данных пользователя
    cursor.execute("SELECT password FROM users WHERE login = ?", (login,))
    user_record = cursor.fetchone()

    # Если пользователь не найден, возвращаем ошибку
    if not user_record:
        return jsonify({'error': 'Пользователь не найден'}), 404

    # Если пароль неверный, возвращаем ошибку
    if user_record[0] != password:
        return jsonify({'error': 'Неверный пароль'}), 401

    # Проверка наличия артикула в таблице 'stock'
    cursor.execute("SELECT * FROM stock WHERE article = ?", (article,))
    article_record = cursor.fetchone()

    # Если артикул не найден, возвращаем ошибку
    if not article_record:
        return jsonify({'error': 'Статья не найдена'}), 404

    # Создание словаря с данными статьи для ответа
    article_data = {'article': article_record[0], 'name': article_record[1], 'price': article_record[2], 'stock': article_record[3]}

    # Освобождение ресурсов
    cursor.close()
    conn.close()

    # Возвращение данных статьи в формате JSON
    return jsonify(article_data)

if __name__ == '__main__':
    app.run(debug=False, port=5000)