from flask import Blueprint, request, jsonify
from utility.db_utils import get_database_connection, check_database_connection

get_article_route = Blueprint('get_article_route', __name__)

# Путь для получения информации по артикулу
@get_article_route.route('/get_article', methods=['POST'])
def get_article():
    cursor = None  # Инициализируем курсор вне блока try

    try:
        # Проверяем и переустанавливаем подключение к базе данных при необходимости
        check_database_connection()

        # Получаем подключение к базе данных
        conn = get_database_connection()

        # Выводим данные запроса для отладки
        # print(request.json)

        # Извлекаем данные из запроса
        data = request.json
        article = data.get('article')
        login = data.get('login')
        password = data.get('password')

        # Создаем курсор для выполнения запросов
        cursor = conn.cursor()

        # Проверяем учетные данные пользователя
        cursor.execute("SELECT password FROM users WHERE login = ?", (login,))
        user_record = cursor.fetchone()
        if not user_record:
            return jsonify({'error': 'Пользователь не найден'}), 404
        if user_record[0] != password:
            return jsonify({'error': 'Неправильный пароль'}), 401

        # Проверяем наличие артикула в таблице 'stock'
       # cursor.execute("SELECT * FROM stok WHERE article = ?", (article,))
       # article_record = cursor.fetchone()
        ## поиск по второй таблице 
        cursor.execute("SELECT * FROM oem WHERE oem = ?", (article,))
        article_record = cursor.fetchone()
        if article_record !=  None:
            cursor.execute("SELECT * FROM stok WHERE article = ?", (article_record[0],))  
            article_record2 = cursor.fetchone()
 
        ##

        if not article_record:
            return jsonify({'error': 'Артикул не найден'}), 404

        # Формируем данные для ответа
        #article_data = {'article': article_record[0], 'name': article_record[1], 'price': article_record[2], 'stock': article_record[3]}
        article_data = {'article': article_record2[0].strip(), 'name': article_record2[1].strip(), 'oem': article_record2[2].strip(), 'year': article_record2[3].strip(), 'price': article_record2[4].strip()}
        
        #article_data = {'article': article_record[0], 'name': article_record[1], 'price': article_record[2]}
        return jsonify(article_data)

    except Exception as e:
        # Обрабатываем исключение
        print('Произошла ошибка:', e)
        # Можно вернуть соответствующий код ошибки здесь
        return jsonify({'error': 'Произошла ошибка'}), 500

    finally:
        if cursor:  # Проверяем, был ли инициализирован курсор
            # Закрываем курсор для освобождения ресурсов
            cursor.close()


test_route = Blueprint('test_route', __name__)

# Тестовый путь для получения статуса работы сервера
@test_route.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({'message': 'Сервер работает'}), 200