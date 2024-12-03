import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from reviews.models import Category


class Command(BaseCommand):
    help = 'Загрузка категорий из CSV файла'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Путь к CSV файлу')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        try:
            with open(csv_file_path, encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)

                with transaction.atomic():
                    for row in csv_reader:
                        # noinspection PyTypeChecker
                        Category.objects.create(
                            name=row['name'],
                            slug=row['slug']
                        )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Успешно загружено категорий: '
                        f'{csv_reader.line_num - 1}'
                    )
                )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Файл не найден: {csv_file_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при загрузке: {str(e)}')
            )
