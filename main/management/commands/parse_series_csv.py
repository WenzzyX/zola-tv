from django.core.management.base import BaseCommand
import csv
from ast import literal_eval
from main.models import (Serie, SerieSeason, SerieEpisode, SerieEpAltLang, Genre, Country, Language)
import time


class Csv_parser:
    def __init__(self, name=""):
        self.file_name = name

    def handler(self):

        with open("import/Series.csv", 'r', encoding="cp1251", errors='ignore') as file:
            reader = csv.DictReader(file, delimiter=';')
            log_entry = []
            for line in reader:
                # print(line)

                link_to_file = "http://api.zola.cx/cdn-cx.php?path="
                link_to_poster = "http://cdn.zola.cx/covers/"
                link_to_ep_poster = "http://cdn.zola.cx/epcovers/"
                link_to_subs = "http://api.zola.cx/cdn-cx.php?path=/subs/"
                serie_name = line['serie_name']
                serie_imdb_id = line['serie_imdb_id']
                serie_genres = literal_eval(line['genres'].strip(' '))
                serie_description = line['description']
                if line['serie_poster_url'] != '':
                    serie_poster = link_to_poster + line['serie_poster_url']
                else:
                    serie_poster = ''
                serie_ep_video_url = link_to_file + line['video_url']
                serie_country = literal_eval(line['country'].strip(' '))
                try:
                    serie_country = serie_country[0][0]
                except IndexError:
                    serie_country = ''
                serie_language = line['language']

                serie_ep_name = line['episode_name']
                serie_s_num = line['season_numbe']
                serie_ep_imdb_id = line['imdb_id']
                serie_ep_num = line['episode_number']
                if line['episode_poster_url'] == line['serie_poster_url']:
                    serie_ep_preview = link_to_poster + line['episode_poster_url']
                else:
                    serie_ep_preview = link_to_ep_poster + line['episode_poster_url']
                try:
                    serie_ep_duration = time.strftime("%H:%M", time.gmtime(int(line['duration'])))
                except:
                    serie_ep_duration = ''
                serie_ep_subtitle = line['subtitle_url']
                if line['subtitle_url'] == 'none.srt':
                    serie_ep_subtitle = ''
                else:
                    serie_ep_subtitle = serie_ep_subtitle.split(',')
                    i = 0
                    for sub in serie_ep_subtitle:
                        serie_ep_subtitle[i] = link_to_subs + sub
                        i += 1
                    serie_ep_subtitle = ','.join(serie_ep_subtitle)
                try:
                    serie_imdb_rating = float(line['imdb_rating'])
                except:
                    serie_imdb_rating = 5.5

                try:
                    serie_year = int(line['year'])
                except:
                    serie_year = 2015
                # break
                try:
                    serie_db = Serie.objects.get(imdb_id=serie_imdb_id)
                    season_db = SerieSeason.objects.get(serie=serie_db, season_num=int(serie_s_num))
                    episode_db = SerieEpisode.objects.get(season=season_db, episode=serie_ep_num)


                    alt_movie_lang = SerieEpAltLang(
                        episode=episode_db
                    )
                    try:
                        alt_movie_lang.language = Language.objects.get(iso3_code=serie_language)
                    except Language.DoesNotExist:
                        pass
                    if alt_movie_lang.language == episode_db.language:
                        log_entry.append('Episode with this lang already exists: ' + serie_name + " ep.: " + serie_ep_name)
                        print('Episode with this lang already exists: ' + serie_name + " ep.: " + serie_ep_name)
                        continue
                    try:
                        alt_ser_lang = SerieEpAltLang.objects.get(episode=episode_db, language=alt_movie_lang.language)
                        log_entry.append('Episode with this ALTlang already exists: ' + serie_name + " ep.: " + serie_ep_name)
                        print('Episode with this ALTlang already exists: ' + serie_name + " ep.: " + serie_ep_name)
                        continue
                    except:
                        alt_movie_lang.video_url = serie_ep_video_url
                        alt_movie_lang.clean_fields()
                        alt_movie_lang.save()
                        log_entry.append(
                            "Added alt lang serie: " + serie_name + " Ep.: " + serie_ep_name + " ; ID: " + serie_imdb_id)
                        print("Added alt lang serie: " + serie_name + " Ep.: " + serie_ep_name + " ; ID: " + serie_imdb_id)
                except (Serie.DoesNotExist, SerieSeason.DoesNotExist, SerieEpisode.DoesNotExist):
                    try:
                        serie_db = Serie.objects.get(imdb_id=serie_imdb_id)
                        try:
                            season_db = SerieSeason.objects.get(serie=serie_db, season_num=int(serie_s_num))
                            try:
                                try:
                                    lang = Language.objects.get(iso3_code=serie_language)
                                except Language.DoesNotExist:
                                    pass
                                episode_db = SerieEpisode.objects.get(season=season_db, episode=serie_ep_num, language=lang)
                            except:

                                episode_db = SerieEpisode(
                                    season=season_db,
                                    episode=serie_ep_num,
                                    episode_name=serie_ep_name,
                                    episode_imdb_id=serie_ep_imdb_id,
                                    preview_url=serie_ep_preview,
                                    video_url=serie_ep_video_url,
                                    duration=serie_ep_duration,
                                    subtitle_urls=serie_ep_subtitle
                                )
                                episode_db.clean_fields()
                                episode_db.save()
                                try:
                                    episode_db.language = Language.objects.get(iso3_code=serie_language)
                                except Language.DoesNotExist:
                                    pass
                                episode_db.save()
                        except Exception as exs:
                            print(exs)
                            season_db = SerieSeason(
                                serie=serie_db,
                                season_num=serie_s_num
                            )
                            print("2!!!!!!CREATED SEASON2!!!!!!", season_db)
                            print(line)
                            season_db.save()
                            episode_db = SerieEpisode(
                                season=season_db,
                                episode=serie_ep_num,
                                episode_name=serie_ep_name,
                                episode_imdb_id=serie_ep_imdb_id,
                                preview_url=serie_ep_preview,
                                video_url=serie_ep_video_url,
                                duration=serie_ep_duration,
                                subtitle_urls=serie_ep_subtitle
                            )
                            episode_db.clean_fields()
                            episode_db.save()
                            try:
                                episode_db.language = Language.objects.get(iso3_code=serie_language)
                            except Language.DoesNotExist:
                                pass
                            episode_db.save()
                    except:
                        serie_db = Serie(
                            name=serie_name,
                            year=serie_year,
                            description=serie_description,
                            poster_url=serie_poster,
                            imdb_id=serie_imdb_id,
                            imdb_rating=serie_imdb_rating,
                            imdb_link='',
                        )
                        serie_db.clean_fields()
                        serie_db.save()
                        serie_db.genre.set(Genre.objects.filter(name__in=serie_genres))
                        try:
                            serie_db.country = Country.objects.get(iso3=serie_country)
                        except Country.DoesNotExist:
                            pass
                        try:
                            serie_db.language = Language.objects.get(iso3_code=serie_language)
                        except Language.DoesNotExist:
                            pass
                        serie_db.save()
                        season_db = SerieSeason(
                            serie=serie_db,
                            season_num=serie_s_num
                        )
                        print("1!!!!!!CREATED SEASON1!!!!!!", season_db)
                        season_db.save()
                        episode_db = SerieEpisode(
                            season=season_db,
                            episode=serie_ep_num,
                            episode_name=serie_ep_name,
                            episode_imdb_id=serie_ep_imdb_id,
                            preview_url=serie_ep_preview,
                            video_url=serie_ep_video_url,
                            duration=serie_ep_duration,
                            subtitle_urls=serie_ep_subtitle
                        )
                        episode_db.clean_fields()
                        episode_db.save()
                        try\
                                :
                            episode_db.language = Language.objects.get(iso3_code=serie_language)
                        except Language.DoesNotExist:
                            pass
                        episode_db.save()
                        # break
                    log_entry.append("Added serie/ep: " + serie_name + " ; ID: " + serie_imdb_id + " ; EPISODE_NAME: " + serie_ep_name)
                    print("Added serie/ep: " + serie_name + " ; ID: " + serie_imdb_id + " ; EPISODE_NAME: " + serie_ep_name)
            with open("import/ser.log", "w", encoding="cp1251", errors='ignore') as file:
                for log in log_entry:
                    file.write(log + '\n')
                file.close()


class Command(BaseCommand):
    help = "Scraping csv"

    def handle(self, *args, **options):
        parser = Csv_parser(name="movies.csv")
        parser.handler()
