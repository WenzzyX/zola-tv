from django.core.management.base import BaseCommand
import csv
from main.models import (Genre)


class Csv_parser:
    def __init__(self, name="csv.csv"):
        self.file_name = name

    def handler(self):

            with open(self.file_name, 'r', encoding="cp1251", errors='ignore') as file:
                reader = csv.DictReader(file, delimiter=',')
                for line in reader:
                    try:
                        genre = Genre.objects.get(name=line['name'])
                        genre.name = line['name']
                        genre.save()
                    except Genre.DoesNotExist:
                        genre = Genre(
                            name=line['name'],
                        )
                        genre.save()


class Command(BaseCommand):
    help = "Scraping csv"

    def handle(self, *args, **options):
        parser = Csv_parser(name="genres.csv")
        parser.handler()
