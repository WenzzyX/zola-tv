from django.core.management.base import BaseCommand
from main.models import Movie, Serie
import requests
import csv
import os


class GetContent:
    def __init__(self, name="csv.csv"):
        self.file_name = name

    def write_log(self, line):
        with open('video_Check.log', 'a', errors='ignore') as file:
            file.write(line + '\n')
            file.close()
        return True

    def write_line(self, file, line):
        try:
            if not os.path.isdir('all_bsh'):
                os.mkdir('all_bsh')
            with open(f"all_bsh/{file}", 'a+', encoding='utf-8', errors='ignore') as file:
                file.write(line + '\n')
                file.close()
        except Exception as e:
            print(e)

    def handler(self, objects, file, type_d='mov'):
        self.write_line(file,
                        f"id~imdb_id~name~year~genres~imdb_rating~poster~imdb_link~country~description~language~duration")
        # name,year,genre,description,imdb_id,poster,rating,duration,date_pub,country,language,imdb_link,show_on_home,objects,
        for obj in objects:
            if type_d == 'mov':
                self.write_line(file,
                                f"{obj.id}~{obj.imdb_id}~{obj.name}~{obj.year}~{','.join(obj.genre.all().values_list('name', flat=True))}~{obj.imdb_rating}~{obj.poster_url}~{obj.imdb_link}~{obj.country}~{obj.description}~{obj.language or None}~{obj.duration}")
            else:
                self.write_line(file,
                                f"{obj.id}~{obj.imdb_id}~{obj.name}~{obj.year}~{','.join(obj.genre.all().values_list('name', flat=True))}~{obj.imdb_rating}~{obj.poster_url}~{obj.imdb_link}~{obj.country}~{obj.description}~{obj.language or None}")

    def main_handler(self):
        # self.write_log('\/---------------------------Movies---------------------------\/')
        self.handler(Movie.objects.all().order_by('id'), file='Movie.csv')
        # self.write_log('\/---------------------------Series---------------------------\/')
        self.handler(Serie.objects.all().order_by('id'), file='Series.csv', type_d="ser")


class Command(BaseCommand):
    help = "Checking imgs"

    def handle(self, *args, **options):
        parser = GetContent(name="countries.csv")
        parser.main_handler()
