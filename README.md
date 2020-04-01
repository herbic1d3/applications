## Постановка задачи ##

_Задача: реализовать API, позволяющее добавлять, изменять, просматривать и удалять данные в модели "Приложения"._
_"Приложения" – это модель, которая хранит в себе внешние источники, которые будут обращаться к API. Обязательные поля модели: ID, Название приложения, Ключ API. Поле "Ключ API" нельзя менять через API напрямую, должен быть метод, позволяющий создать новый ключ API._
_После добавления приложения – должна быть возможность использовать "Ключ API" созданного приложения для осуществления запросов к метод /api/test, метод должен возвращать JSON, содержащий всю информацию о приложении._

_Использовать следующие технологии: Django 2.2.7, Django REST framework._

_Результат выполнения задачи:_
_- исходный код приложения в github_
_- инструкция по разворачиванию приложения (в docker или локально)_
_- инструкция по работе с запросами к API: как авторизоваться, как добавить, как удалить и т.д._

## Установка ##

Установка приложения производится с помощью `Docker Compose` инструментального средства, входящящего в состав `Docker`.
Тестировалось с использованием:

* `docker-compose` - version 1.25.1-rc1
* `docker` - version 19.03.8

#### Последовательность действий ####

1. Клонировать исходный код приложения на целевую машину командой:
`https://bitbucket.org/herbic1d3/applications/`
2. Изменить значений переменных по умолчанию, при необходимости, в файле `/<каталог приложения>/build/app.env`
3. Изменить значение порта, по которому будет доступно приолжение, в файле `docker-compose.yml`, при необходимости, порт по умолчанию `8000` 
3. Выполнить установку и развертывание приложения командой `docker-compose up -d --build`
При локальной установке, приложение доступно по адресу `http://localhost:8000`.
Проверить корректность установки и работоспособность приложения можно выполнив команду `docker-compose exec web python /app/manage.py test`, успешный вариант выполнения выглядит как 

````
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
-----------------------------------------------------------
Ran 7 tests in 2.020s

OK
Destroying test database for alias 'default'...
````
 

## Конфигурирование ##

Первончальная конфигурация приложения производится через админ панель, доступную по адресу `http://localhost:8000/admin`, данные для авторизации содержатся в файле ``/<каталог приложения>/build/app.env`` значения по умолчанию:
* `username` - admin
* `password` - qwerty
 
#### Возможности админ панели ####
 
 * Создание пользователей
 * Создание API ключей
 * Создание приложений с указаним API ключа доступа и списка urls внешних источников.
 
## Использование ##

Использование приложения производится с помощью доступа к API
Для первоначального использование необходимо произвести по имени пользователя и паролю, для получения токена доступа, пример:

_запрос_

```
POST http://localhost:8000/api-token-auth/ HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=<username>&password=<password>
```

_ответ_

```
Content-Type: application/json
Allow: POST, OPTIONS
X-Frame-Options: SAMEORIGIN
Content-Length: 52

{
  "token": "e6c0332fb083d7a3655474470c714265825bee42"
}

Response code: 200 (OK); Time: 223ms; Content length: 52 bytes
```

#### Команды и API ####

#### Вся информация о приложении ####

* url: `/api/test/<access key>/` 
* access method GET
* response: 
    * status code: 200
    * application/json
    * data: 
[
    {'id': <id_1>,'title': <title_1>, 'created': <created datetime>}
    ...
    {'id': <id_N>,'title': <title_N>, 'created': <created datetime>}
]

пример:

_запрос_

```
GET http://localhost:8000/api/test/ee36d1bb-3082-42f9-b2cd-011e0893dc4f HTTP/1.1
Authorization:  Token 934d458e0b9d10e90f1d0b00ca646c1d8a925511
```

_ответ_

```
Content-Type: application/json
Vary: Accept
Allow: GET, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
Content-Length: 77

[
  {
    "id": 1,
    "title": "test application",
    "created": "2020-04-01T12:51:12.851840Z"
  }
]

Response code: 200 (OK); Time: 78ms; Content length: 77 bytes
```

#### Создание приложения ####

* url: `/api/` 
* access method POST
* request: {'key': <access key>, 'title': <new application title>}
* response: status code: 201, application/json
    * data: {'id': <created application id>, 'title': <new application title>, 'key': <access key>}

#### Обновление приложения ####

* url: `/api/<application id>/` 
* access method PUT
* request: {'key': <access key>, 'title': <new application title>}
* response: status code: 200, application/json
    * data: {'id': <created application id>, 'title': <new application title>, 'key': <access key>}

#### Удаление приложения ####

* url: `/api/<application id>/` 
* access method DELETE
* request: {''key': <access key>}
* response: status code: 204










