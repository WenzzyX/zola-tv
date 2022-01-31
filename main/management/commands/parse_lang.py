from django.core.management.base import BaseCommand
import csv
from ast import literal_eval
from main.models import (Movie, Genre, Country, Language)
import time


class Csv_parser:
    def __init__(self, name=""):
        self.file_name = name

    def handler(self):
        a = """
        eng  45  English
        hin  770  Hindi
        tel  675  Telugu
        mal  425  Malayalam
        ben  100  Bengali
        tam  655  Temil
        urd  730  Urdu
        ind  210  indonesian
        chi  315  Chinese
        fre  745  French
        tha  645  Thai
        spa  230  Spanish
        rus  570  Russian
        fas  535  Farsi
        ger  481  German
        ita  235  Italian
        jpn  870  Japaneese
        kor  330  Korean
        lao  375  Lao
        mar  440  Marathi
        pan  530  Punjabi
        por  545  Portuguese
        """
        lista = a.split('\n')
        i = 0
        for el in lista:
            fin = el.strip().split(' ')
            o = 0
            for elem in fin:
                if elem == '':
                    del fin[o]
                o += 1
            if fin != [] and fin != '':
                lista[i] = fin

            i += 1
        del lista[0]
        del lista[-1]

        for saves in lista:
            lan = Language(
                name=saves[2],
                iso3=saves[0],
                iso3_code=saves[1]
            )
            lan.save()
        print(lista)


class Command(BaseCommand):
    help = "Scraping csv"

    def handle(self, *args, **options):
        parser = Csv_parser(name="movies.csv")
        parser.handler()
