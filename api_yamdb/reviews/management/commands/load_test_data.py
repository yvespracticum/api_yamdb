import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ("Load all data: categories, genres, titles, and genre-title "
            "relations.")

    def handle(self, *args, **kwargs):
        commands = [
            ["python", "manage.py", "load_categories",
             "static/data/category.csv"],
            ["python", "manage.py", "load_genres", "static/data/genre.csv"],
            ["python", "manage.py", "load_titles", "static/data/titles.csv"],
            ["python", "manage.py", "load_genre_title",
             "static/data/genre_title.csv"],
        ]

        for command in commands:
            self.stdout.write(
                self.style.NOTICE(f"Running command: {' '.join(command)}")
            )
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                self.stdout.write(self.style.SUCCESS(result.stdout.strip()))
            else:
                self.stderr.write(self.style.ERROR(result.stderr.strip()))
                break
