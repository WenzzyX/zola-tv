from django.core.management.base import BaseCommand
import csv
from main.models import (Subtitle)


class Csv_parser:
    def __init__(self, name="csv.csv"):
        self.file_name = name

    def handler(self):

            with open(self.file_name, 'r', encoding="cp1251", errors='ignore') as file:
                reader = csv.DictReader(file, delimiter=';')
                for line in reader:

                    file_extension = line['fileformat']
                    file_name = line['filename']
                    language = line['lang']
                    try:
                        subtitle = Subtitle.objects.get(file_name=file_name, language=language)
                        print(f"already exists: {file_name}")
                        continue
                    except Subtitle.DoesNotExist:
                        sub = Subtitle(
                            file_name=file_name,
                            file_extension=file_extension,
                            language=language
                        )
                        print(f"added sub: {file_name}")
                        sub.save()


class Command(BaseCommand):
    help = "Scraping csv"

    def handle(self, *args, **options):
        parser = Csv_parser(name="import/subtitles.csv")
        parser.handler()
