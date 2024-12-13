# Проект YaMDb

## Описание
YaMDb — это платформа для сбора отзывов пользователей на произведения из различных категорий, таких как книги, фильмы, музыка и другие.

> **Важно**: Сами произведения (например, фильмы или музыкальные записи) на платформе не хранятся.

## Функционал
1. Создание отзывов на произведения с оценками (от 1 до 10).
2. Комментирование отзывов.
3. Поддержка усреднённого рейтинга для произведений.
4. Группировка произведений по категориям ("Книги", "Фильмы", "Музыка" и др.).
5. Использование предустановленных жанров (например, "Сказка", "Рок", "Артхаус").
6. Регистрация, авторизация пользователей через JWT-токены.

## Стек технологий
- Python 3.9+
- Django 3.2
- Django REST Framework 3.12.4
- Simple JWT 4.7.2
- SQLite

## Как развернуть проект

1. Клонировать репозиторий:
```bash
git clone https://github.com/yvespracticum/api_yamdb.git
cd api_yamdb
```
2. Убедиться, что установлен Python (рекомендуется версия 3.9+).
3. Установить виртуальное окружение:
```bash
python3 -m venv .venv
source .venv/bin/activate  # для Linux/MacOS
.venv\Scripts\activate  # для Windows
```
4. Установить зависимости:
```bash
pip install -r requirements.txt
```
5. Выполнить миграции базы данных:
```bash
python manage.py migrate
```
6. Запустить локальный сервер разработки:
```bash
python manage.py runserver
```

>Для тестирования функционала, можно загрузить тестовые данные в базу данных используя команду:
>```bash
>python manage.py load_test_data
>```

---

## Документация

Документация после запуска сервера будет доступна по адресу:
```
http://127.0.0.1:8000/redoc/
```

Она предоставляет примеры всех доступных запросов к API.

### Примеры запросов:

#### 1. Получение списка всех книг в жанре сказки

Запрос:
```http
GET /api/v1/titles/?category=book&genre=tale
```

Ответ:
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 20,
      "name": "Колобок",
      "year": 1873,
      "rating": null,
      "description": "",
      "genre": [
        {
          "name": "Триллер",
          "slug": "thriller"
        },
        {
          "name": "Сказка",
          "slug": "tale"
        }
      ],
      "category": {
        "name": "Книга",
        "slug": "book"
      }
    },
    {
      "id": 25,
      "name": "Винни Пух и все-все-все",
      "year": 1926,
      "rating": null,
      "description": "",
      "genre": [
        {
          "name": "Сказка",
          "slug": "tale"
        }
      ],
      "category": {
        "name": "Книга",
        "slug": "book"
      }
    }
  ]
}
```

#### 2. Создание нового отзыва

Запрос:
```http
POST /api/v1/titles/{title_id}/reviews/
```

Тело запроса:
```json
{
    "text": "Это лучший фильм, который я видел!",
    "score": 10
}
```

Ответ:
```json
{
    "id": 1,
    "text": "Это лучший фильм, который я видел!",
    "author": "user1",
    "score": 10,
    "pub_date": "2024-12-12T12:34:56.789",
    "title": 1
}
```

---

## Авторы

Проект разработан участниками:

- [Валерия Рабченюк](https://github.com/ValeryRabchenyuk)
- [Олег Мартьянов](https://github.com/OlegMorty)
- [Иван Подгорный](https://github.com/yvespracticum)

