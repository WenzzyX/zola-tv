from django.core.management.base import BaseCommand
import csv
from main.models import (Country)


class Csv_parser:
    def __init__(self, name="csv.csv"):
        self.file_name = name

    def handler(self):

        with open(self.file_name, 'r', encoding="cp1251", errors='ignore') as file:
            reader = csv.DictReader(file, delimiter=',')
            for line in reader:
                print(line['name'])
                try:
                    country = Country.objects.get(iso3=line['ISO3'])
                    country.name = line['name']
                    country.iso3 = line['ISO3']
                    country.save()
                except Country.DoesNotExist:
                    country = Country(
                        name=line['name'],
                        iso3=line['ISO3'],
                    )
                    country.save()


class Command(BaseCommand):
    help = "Scraping csv"

    def handle(self, *args, **options):
        parser = Csv_parser(name="countries.csv")
        parser.handler()
