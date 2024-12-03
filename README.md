Загрузить данные в базу из csv файлов можно командами:

```shell
# категории:
python manage.py load_categories static/data/category.csv
# жанры:
python manage.py load_genres static/data/genre.csv
# произведения:
python manage.py load_categories static/data/titles.csv
# связи произведение-жанр:
python manage.py load_genre_title static/data/genre_title.csv
```
