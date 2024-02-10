import pyodbc
import os

# Глобальная переменная для хранения подключения к базе данных
_db_connection = None

def setup_database_connection():
    global _db_connection
    try:
        if _db_connection is None:
            print(0)
            # Получаем строку подключения к базе данных из файла .env
            db_connection_string = os.getenv('DB_CONNECTION_STRING')

            # Устанавливаем подключение к базе данных
            _db_connection = pyodbc.connect(db_connection_string)

            # Проверяем подключение к базе данных с помощью простого запроса
            cursor = _db_connection.cursor()
            cursor.execute('SELECT 1')
            cursor.close()

            print('Успешное подключение к базе данных')

    except Exception as e:
        print('Ошибка при установке подключения к базе данных:', e)

def get_database_connection():
    global _db_connection
    return _db_connection

def check_database_connection():
    global _db_connection
    try:
        if not _db_connection or _db_connection.closed:
            # Переустанавливаем подключение к базе данных
            setup_database_connection()

    except pyodbc.Error as e:
        print('Ошибка подключения к базе данных:', e)
        raise