from django.core.management.base import BaseCommand
from main.models import Movie, Serie, Show, SerieEpisode, ShowEpisode, Channel
import requests


class ImgChecker:
    def __init__(self, name="csv.csv"):
        self.file_name = name

    def write_log(self, line):
        with open('Img_Check.log', 'a', errors='ignore') as file:
            file.write(line + '\n')
            file.close()
        return True

    def handler(self, objects, type_p):
        session = requests.session()
        for object in objects:
            if type_p == 'DModel':
                poster_url = object.get_poster()
                imdb_id = object.imdb_id
            elif type_p == "Episode":
                poster_url = object.get_preview()
                imdb_id = object.episode_imdb_id
            elif type_p == "Channel":
                poster_url = object.get_preview()
                imdb_id = object.id
            try:
                request = session.head(url=poster_url)
                if request.status_code != 200:
                    self.write_log(
                        f'IMDB-ID: {imdb_id} , Img-Not-Found: {poster_url} , Error-code: {request.status_code}')
                    print(f'IMDB-ID: {imdb_id} img-n-f, {type_p}')
            except Exception as e:
                self.write_log(
                    f'IMDB-ID: {imdb_id}, Link-error: {poster_url} , Error-code: invalid link exception')
                print('error-url', e)

    def main_handler(self):
        self.write_log('\/---------------------------Movies---------------------------\/')
        self.handler(Movie.objects.all().order_by('imdb_id'), type_p='DModel')
        self.write_log('\/---------------------------Series---------------------------\/')
        self.handler(Serie.objects.all().order_by('imdb_id'), type_p='DModel')
        self.write_log('\/---------------------------Shows---------------------------\/')
        self.handler(Show.objects.all().order_by('imdb_id'), type_p='DModel')
        self.write_log('\/---------------------------SerieEpisodes---------------------------\/')
        self.handler(SerieEpisode.objects.all().order_by('episode_imdb_id'), type_p='Episode')
        self.write_log('\/---------------------------ShowEpisodes---------------------------\/')
        self.handler(ShowEpisode.objects.all().order_by('episode_imdb_id'), type_p='Episode')
        self.write_log('\/---------------------------Channel---------------------------\/')
        self.handler(Channel.objects.all(), type_p='Channel')


class Command(BaseCommand):
    help = "Checking imgs"

    def handle(self, *args, **options):
        parser = ImgChecker(name="countries.csv")
        parser.main_handler()
