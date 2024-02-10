# stock-api

# Оглавление

1. [Предварительные требования](#предварительные-требования)
2. [Начало работы](#начало-работы)
    - [Копирование проекта с GitHub](#копирование-проекта-с-github)
    - [Настройка файла .env](#настройка-файла-env)
    - [Установка зависимостей](#установка-зависимостей)
    - [Запуск программы](#запуск-программы)
3. [Описание метода POST](#описание-метода-post)
4. [Настройка телеграм бота](#настройка-телеграм-бота)
5. [Синхронизация репозитория](#синхронизация-репозитория)

## Предварительные требования

Для работы с проектом вам потребуется:

- Python 3.6 или выше
- MS SQL Server
- (Опционально) SQL Server Management Studio (SSMS) для управления базой данных

## Начало работы

Для начала работы с проектом выполните следующие шаги.

### Копирование проекта с GitHub

1. Убедитесь в том, что Python установлен с помощью команды ```python --version```
2. Склонируйте репозиторий на локальную машину с помощью команды: ```git clone https://github.com/ecspecial/stock-api.git```
3. Перейдите в директорию проекта: ```cd stock-api```

### Настройка файла .env
1. Добавьте в файл `.env` строки со значениями переменных окружения для подключения к базе данных
2. Замените `localhost\SQLEXPRESS`, `test`, `ваш_логин` и `ваш_пароль` (при подключении через логин и пароль) на актуальные значения для вашей среды

### Установка зависимостей

1. Создайте виртуальное окружение и активируйте его:

- Для Windows:

  ```
  python -m venv venv
  .\venv\Scripts\activate
  ```

- Для macOS и Linux:

  ```
  python3 -m venv venv
  source venv/bin/activate
  ```

2. Установите необходимые пакеты из файла `requirements.txt` с помощью команды: ```pip install -r requirements.txt```

### Запуск программы

Запустите приложение с помощью команды: ```python .\src\stock-api\stock_server.py```


## Описание метода POST

Метод `POST /get_article` предназначен для получения информации о товаре по его артикулу. Для использования метода необходимо отправить JSON-запрос со следующей структурой:

Тестирование можно проводить при помощи Postman, отправляя запросы на адрес http://localhost:5000/get_article

```json
{
  "article": "артикул_товара",
  "login": "ваш_логин",
  "password": "ваш_пароль"
}

Если указанный логин и пароль верны, и товар с указанным артикулом существует в базе данных, метод вернет JSON-ответ с информацией о товаре:
{
  "article": "артикул",
  "name": "название",
  "price": "цена",
  "stock": "количество на складе"
}

В случае ошибки (например, неверный логин/пароль или товар не найден) метод вернет соответствующее сообщение об ошибке.
```


## Настройка телеграм бота

1. Открыть менеджер ботов [@BotFather](https://t.me/BotFather) в Telegram
2. Запустить бота командой `/start`
3. Запустить процесс создания нового бота командо `/newbot`
4. Ввести нащвание бота
5. Ввести юзернейм бота
6. Из сообщения о готовности бота скопировать токен бота, пример `11111111:OOjjdHHDKMjdc7Slkkfvkm489fvfJld`
7. - Создать новый канал в телеграм (публичный)
   - Зайти в управление каналом
   - Выбрать вкладку Администраторы
   - Добавить в администраторы созданного бота по его нику, например, @TestBot
8. Получить id нашего канала, отправив тестовое сообщение через браузер:
   - В браузере в поисковой строке ввести ссылку с полученным токеном бота и названием нашего канала, например, @TestChannel`https://api.telegram.org/bot11111111:OOjjdHHDKMjdc7Slkkfvkm489fvfJld/sendMessage?chat_id=@TestChannel&text=test`
   - Отправить запрос
   - Из ответа скопировать id в обьекте chat, например `-100193333734` в полученном ответе `"chat":{"id":-100193333734,"title":"@TestChannel","username":"TestChannel","type":"channel"},"date":1708891756,"text":"test"}}`
9. В файл .env вставить строки с полученными значениями токена бота и id нашего канала
   - `TELEGRAM_CHAT_ID='-100193333734`
   - `TELEGRAM_BOT_TOKEN='11111111:OOjjdHHDKMjdc7Slkkfvkm489fvfJld`
10. При желании запустить отслеживание работы нашего сервера в новом окне терминала командой ```python .\src\telegram-api\telegram_server.py``` из главной директории stock-api


## Синхронизация репозитория

Для синхронизации локального репозитория с обновленным репозиторием на GitHub выполните команду ```git pull``` и повторно выполните установку модулей ```pip install -r requirements.txt``` 