import os
from flask import Flask
from dotenv import load_dotenv
from routes.routes import get_article_route, test_route
from utility.db_utils import setup_database_connection

app = Flask(__name__)

# Загрузка переменных окружения из файла .env
load_dotenv()

# Инициализация подключения к базе данных при запуске приложения
setup_database_connection()

# Регистрация маршрутов
app.register_blueprint(get_article_route)
app.register_blueprint(test_route)

if __name__ == '__main__':
    # Запуск приложения
    app.run(debug=False, port=5000)