## FSTRPereval Django REST API
### Описание
REST API написанный на python использующий Django REST framework для реализации работы с базой данных на PostgreSQL.
API реализует возможность получать список перевалов, детали о перевале, загружать перевалы и изменять уже загруженные перевалы. Доступна Swagger документация.
Так же доступна онлайн версия на хосте pythonanywhere: https://alexeivar.pythonanywhere.com подробности ниже.
#### Стэк
- Django
- Django Rest Framework
- DRF Writable Nested
- Django REST Swagger
- Json
- Dotenv

### Установка
Код написан на python 3.12, на сервере работает 3.10, поддержка других версий не гарантированна.
После скачивания репозитория нужно установить необходимые модули из requirements.txt.
Для работы из коробки нужно предоставить доступ к базе данных PostgreSQL с названием pereval, в .env предоставить логин(FSTR_DB_LOGIN), пароль(FSTR_DB_PASS), хост(FSTR_DB_HOST) и порт(FSTR_DB_PORT).

### Структура хранения данных
Путем нескольких модулей реализовано хранение данных о перевале и пользователях.
У пользователей (модель CustomUser) хранятся:
- phone - номер телефона, charfield длинной в 16
- fam - фамилия, charfield длинной в 50
- name - имя, charfield длинной в 50
- otc - отчество, charfield длинной в 50
- email - почта, emailField

Хранение данных о перевалах разделено на 4 модели
1. Level
	хранит в себе данные об уровне сложности перевала по времени года:
	- winter - зима, charfield длинной в 2, может быть пустым
	- summer - лето, charfield длинной в 2, может быть пустым
	- autumn - осень, charfield длинной в 2, может быть пустым
	- spring - весна, charfield длинной в 2, может быть пустым
2. Coords
	хранит координаты перевала, включая его высоту:
	- latitude - широта, floatfield
	- longitude - долгота, floatfield
	- height - высота, integerfield
3. Images
	хранит изображения перевала, каждое изображение имеет 3 значения
	- data - дата изображения (в целях обучения оставлен как charfield, однако предусматривает хранение ссылки как urlfield)
	- title - название 
	- pereval - перевал с которым связанно изображение
4. Pereval
	хранит название перевала и связывает все остальные данные:
	- add_time - время добавление, datetimefield с автоматическим добавлением
	- beauty_title - титул (например пер.), charfield длинной в 25
	- title - название, charfield длинной в 25
	- other_titles - другие названия, charfield длинной в 25
	- connect - соединение между строками, charfield длинной в 25, может быть пуст
	- status - статус модерации, charfield длинной в 8, по умолчанию стоит NE, статус выбирается из 4 (NE, PE, AC, RE) при помощи choices
	- level - уровень сложности, foreignkey к level
	- coords - координаты, foreignkey к coords
	- user - пользователь отправивший перевал, foreignkey к user

### Использование
#### Swagger
По пути /docs/ доступна Swagger документация.
#### list и post
По пути /perevals/ доступен список перевалок.
По тому же пути возможно отправка post запроса используя json следующего формата:
```json
{
    "beauty_title": "пер. ",
    "title": "Пхия",
    "other_titles": "Триев",
    "connect": "",
    "user": {
        "email": "qwerty@mail.ru",
        "fam": "Пупкин",
        "name": "Васильевич",
        "otc": "Иванович",
        "phone": "+7 555 55 55"
    },
    "coords": {
        "latitude": "45.3842",
        "longitude": "7.1525",
        "height": "1200"
    },
    "level": {
        "winter": "",
        "summer": "1А",
        "autumn": "1А",
        "spring": ""
    },
    "images": [
        {
            "data": "<картинка1>",
            "title": "Седловина"
        },
        {
            "data": "<картинка>",
            "title": "Подъём"
        }
    ]
}
```
В случае успеха отправляется статус HTTP 200 OK вместе с сообщением "Отправлено успешно" и id созданного перевала.
В случае провала отправляется статус HTTP 400 BAD REQUEST вместе с ошибками.
#### GET и PATCH
По пути /pereval/{ID} можно получить данные об определенном перевале, ответ будет в виде json следующего формата:
```json
{
    "id": 1,
    "add_time": "2024-10-21T11:40:35.880630Z",
    "beauty_title": "пер.",
    "title": "Пхия",
    "other_titles": "Триев",
    "connect": "",
    "status": "NE",
    "level": {
        "winter": "",
        "summer": "1А",
        "autumn": "1А",
        "spring": ""
    },
    "coords": {
        "latitude": 45.3842,
        "longitude": 7.1525,
        "height": 1200
    },
    "images": [
        {
            "data": "<картинка1>",
            "title": "Седловина"
        },
        {
            "data": "<картинка>",
            "title": "Подъём"
        }
    ],
    "user": {
        "phone": "+7 555 55 55",
        "email": "qwerty@mail.ru",
        "fam": "Пупкин",
        "name": "Васильевич",
        "otc": "Иванович"
    }
}
```
Отсюда же можно отправить PATCH запрос, запрос PUT недоступен. 
PATCH принимает такой же JSON что и POST, но так же принимает и отдельные значения в формате JSON, как пример:
```json
{"beauty_title": "per."}
```
приведет к смене только одного значения.
В качестве ответа PATCH вернет state, 0 означает что данные не перезаписаны, 1 означает успех. Если state 0, то так же будет отправлено сообщение с описанием проблемы.
PATCH нельзя использовать для смены данных пользователя. 
PATCH нельзя использовать если статус перевала не равен NE.

### Сервер
При помощи хоста pythonanywhere был запущен сервер с API, однако он использует SQlite для базы данных, поскольку PostgreSQL требует платной подписки.
Сервер доступен по адресу https://alexeivar.pythonanywhere.com/
Для list и post адрес https://alexeivar.pythonanywhere.com/perevals/
Для get и patch адрес https://alexeivar.pythonanywhere.com/perevals/1 (если ID 1)
Документация swagger доступна по адресу https://alexeivar.pythonanywhere.com/docs/
