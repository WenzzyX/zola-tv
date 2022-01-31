from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
import requests, bs4, re, fake_useragent
from time import sleep
from main.models import (Movie, Show, Serie, Genre)


class ImdbParser:
    def __init__(self, url="https://www.imdb.com/chart/top/?ref_=nv_mv_250", count=10):
        self.parse_url = url
        self.parse_count = count
        self.home_url = "https://www.imdb.com/"
        self.session = requests.session()
        self.session.headers = {
            "User-Agent": fake_useragent.UserAgent().random,
            "Accept-Language": "en-US,en;q=0.5"
        }

    def get_page(self, url):
        page = self.session.get(url)
        sleep(1)
        return page.text

    def handler(self):
        html = self.get_page(self.parse_url)
        soup = bs4.BeautifulSoup(html, "lxml")
        container = soup.find('tbody', class_="lister-list")
        progress = 1
        all_cards = container.find_all('tr')[:self.parse_count]
        # all_data = []
        for media in all_cards:
            name = media.find('td', class_='titleColumn').find('a').get_text()
            year = re.search(r'(\d+)', media.find('span', class_='secondaryInfo').get_text()).group(0)
            image = re.sub(r'^(.+)@(.+)$', r'\1@._V1.jpg', media.find('img').get('src'))
            rating = media.find('strong').get_text()
            imdb_id = (media.find('div', class_='wlb_ribbon').get('data-tconst')).replace('tt', '')
            link = f'{self.home_url}title/tt{imdb_id}'
            inner_html = self.get_page(link)
            inner_soup = bs4.BeautifulSoup(inner_html, 'lxml')
            body = inner_soup.find('body').get('class')
            genres = []
            if (body == ['fixed']):  # OLD
                # print("OLD")
                description = inner_soup.find('div', class_='inline canwrap').find('span').get_text()
                genres.append((
                                  (inner_soup.find_all('div', class_='see-more inline canwrap')[1]).find(
                                      'a').get_text()).strip())
            elif (body == None):  # NEW
                # print("NEW")
                description = inner_soup.find('div', class_='ipc-html-content ipc-html-content--base').find(
                    'div').get_text()
                try:
                    # with open("newimdb.html", "w", encoding="utf-8") as file:
                    #     file.write(str(r))
                    #     file.close()
                    for genre in inner_soup.find('div',
                                                 class_='GenresAndPlot__GenresChipList-cum89p-7').find_all(
                        'a'):
                        # print(genre)
                        genres.append(genre.find('span').get_text())
                except AttributeError:
                    genres.append('')

            print('PROGRESS: ', progress, ' of ', len(all_cards), f' Movie: "{name}"', genres)
            data = {
                'name': name,
                'year': year,
                'image': image,
                'description': description,
                'genres': genres,
                'rating': rating,
                'imdb_id': imdb_id,
                'link': link
            }
            try:
                movie_db = Serie.objects.get(imdb_id=imdb_id)
                movie_db.name = name
                movie_db.year = year
                movie_db.description = description
                movie_db.imdb_poster = image
                movie_db.genre.set(Genre.objects.filter(name__in=genres))
                movie_db.imdb_rating = rating
                movie_db.imdb_id = imdb_id
                movie_db.imdb_link = link
                movie_db.save()
            except Serie.DoesNotExist:
                movie_db = Serie(
                    name=name,
                    year=year,
                    description=description,
                    poster_url=image,
                    imdb_id=imdb_id,
                    imdb_rating=rating,
                    imdb_link=link
                )
                # movie_db.genre.add()
                movie_db.save()
                movie_db.genre.set(Genre.objects.filter(name__in=genres))
                movie_db.save()
            progress += 1


class Command(BaseCommand):
    help = "Scraping IMDB"

    def handle(self, *args, **options):
        parser = ImdbParser(url="https://www.imdb.com/chart/tvmeter/?ref_=nv_tvv_mptv", count=30)
        parser.handler()
