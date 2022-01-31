from django.core.management.base import BaseCommand
from main.models import Movie, Serie, Show, SerieEpisode, ShowEpisode, Channel, Sport
import requests
import csv
import os


class ImgChecker:
    def __init__(self, name="csv.csv"):
        self.file_name = name

    def write_log(self, line):
        with open('video_Check.log', 'a', errors='ignore') as file:
            file.write(line + '\n')
            file.close()
        return True
    def write_line(self, file, line):
        try:
            if not os.path.isdir('all_cont_p'):
                os.mkdir('all_cont_p')
            with open(f"all_cont_p/{file}", 'a+', encoding='utf-8', errors='ignore') as file:
                file.write(line + '\n')
                file.close()
        except Exception as e:
            print(e)

    def handler(self, objects, file, type_d='mov'):
        self.write_line(file, f"id;name;file")
        for obj in objects:
            if type_d == 'sep':
                self.write_line(file, f"{obj.id};{obj.episode_name};{obj.get_video()}")
            else:
                self.write_line(file, f"{obj.id};{obj.name};{obj.get_video()}")

    def main_handler(self):
        # self.write_log('\/---------------------------Movies---------------------------\/')
        self.handler(Movie.objects.all().order_by('id'), file='Movie.csv')
        # self.write_log('\/---------------------------SerieEpisodes---------------------------\/')
        self.handler(SerieEpisode.objects.all().order_by('id'), file='SerieEp.csv', type_d='sep')
        # self.write_log('\/---------------------------ShowEpisodes---------------------------\/')
        self.handler(ShowEpisode.objects.all().order_by('id'), file='ShowEp.csv', type_d='sep')
        # self.write_log('\/---------------------------Channel---------------------------\/')
        self.handler(Channel.objects.all(), file='Channel.csv')
        # self.write_log('\/---------------------------Sport---------------------------\/')
        self.handler(Sport.objects.all(), file='Sport.csv')


class Command(BaseCommand):
    help = "Checking imgs"

    def handle(self, *args, **options):
        parser = ImgChecker(name="countries.csv")
        parser.main_handler()
