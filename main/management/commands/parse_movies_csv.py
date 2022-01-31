from django.core.management.base import BaseCommand
import csv
from ast import literal_eval
from main.models import (Movie, MovieAltLang, Genre, Country, Language)
import time


class Csv_parser:
    def __init__(self, name=""):
        self.file_name = name

    def handler(self):

        with open("import/movies.csv", 'r', encoding="cp1251", errors='ignore') as file:
            reader = csv.DictReader(file, delimiter=';')
            log_entry = []
            for line in reader:
                link_to_file = "http://api.zola.cx/cdn-cx.php?path="
                link_to_poster = "http://cdn.zola.cx/covers/"
                link_to_subs = "http://api.zola.cx/cdn-cx.php?path=/subs/"

                film_genres = literal_eval(line['genres'].strip(' '))
                film_country = literal_eval(line['country'].strip(' '))
                try:
                    film_country = film_country[0]
                except IndexError:
                    film_country = ''
                try:
                    film_duration = time.strftime("%H:%M", time.gmtime(int(line['duration'])))
                except:
                    film_duration = ''
                film_poster = link_to_poster + line['imdb_id'] + '.jpg'
                film_video_url = link_to_file + line['video_ur']
                film_subtitles = line['subtitle_url']
                if line['subtitle_url'] == 'none.srt':
                    film_subtitles = ''
                else:
                    film_subtitles = film_subtitles.split(',')
                    i = 0
                    for sub in film_subtitles:
                        film_subtitles[i] = link_to_subs + sub
                        i += 1
                    film_subtitles = ','.join(film_subtitles)
                try:
                    film_imdb_rating = float(line['imdb_rating'])
                except:
                    film_imdb_rating = 5.5

                try:
                    film_year = int(line['year'])
                except:
                    film_year = 2015
                # print(film_country, film_video_url)
                # break
                # name, year, genres, description, imdb_id, imdb_rating, poster_url, video_url, duration,country, language, imdb_link
                try:
                    movie_db = Movie.objects.get(imdb_id=line['imdb_id'].strip(' '))

                    alt_movie_lang = MovieAltLang(
                        movie=movie_db
                    )
                    try:
                        alt_movie_lang.language = Language.objects.get(iso3_code=line['language'].strip(' '))
                    except Language.DoesNotExist:
                        pass
                    if alt_movie_lang.language == movie_db.language:
                        log_entry.append(
                            "Film with this lang already exists: " + line['film_name'].strip(' ') + " ; ID: " + line['imdb_id'] + " ; lang: " + line['language'].strip(' '))
                        print('Film with this lang already exists')
                        continue
                    try:
                        alt_mt_lang = MovieAltLang.objects.get(movie=movie_db, language=alt_movie_lang.language)
                        log_entry.append(
                            "Film with this ALTlang already exists: " + line['film_name'].strip(' ') + " ; ID: " + line[
                                'imdb_id'] + " ; lang: " + line['language'].strip(' '))
                        print('Film with this ALTlang already exists')
                        continue
                    except:
                        alt_movie_lang.video_url = film_video_url
                        alt_movie_lang.clean_fields()
                        alt_movie_lang.save()
                        log_entry.append(
                            "Added alt lang film: " + line['film_name'].strip(' ') + " ; ID: " + line['imdb_id'] + " ; lang: " + line['language'].strip(' '))
                except Movie.DoesNotExist:
                    print(line['imdb_id'])
                    movie_db = Movie(
                        name=line['film_name'].strip(' '),
                        year=film_year,
                        description=line['description'].strip(' '),
                        poster_url=film_poster.strip(' ').replace(' ', ''),
                        video_url=film_video_url,
                        duration=film_duration,
                        imdb_id=line['imdb_id'],
                        imdb_rating=film_imdb_rating,
                        imdb_link=line['imdb_url'].strip(' ').replace(' ', ''),
                        subtitle_urls=film_subtitles
                    )
                    try:
                        movie_db.clean_fields()
                    except:
                        continue
                    movie_db.save()
                    movie_db.genre.set(Genre.objects.filter(name__in=film_genres))
                    try:
                        movie_db.country = Country.objects.get(iso3=film_country)
                    except Country.DoesNotExist:
                        pass
                    try:
                        movie_db.language = Language.objects.get(iso3_code=line['language'].strip(' '))
                    except Language.DoesNotExist:
                        pass
                    movie_db.save()
                    log_entry.append("Added film: " + line['film_name'].strip(' ') + " ; ID: " + line['imdb_id'] + " ; lang: " + line['language'].strip(' '))
            with open("import/mov.log", "w", encoding="cp1251", errors='ignore') as file:
                for log in log_entry:
                    file.write(log + '\n')
                file.close()


class Command(BaseCommand):
    help = "Scraping csv"

    def handle(self, *args, **options):
        parser = Csv_parser(name="movies.csv")
        parser.handler()
