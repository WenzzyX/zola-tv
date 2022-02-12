from django.db import models
from django.db.models import Q
from datetime import datetime
from django.utils.timezone import now
from django.contrib.contenttypes.fields import GenericRelation


# +++++++++++++++++++ MANAGERS +++++++++++++++++++

class GenreManager(models.Manager):
    """ GENRE MANAGER """

    def get_queryset(self):
        return super().get_queryset()

    def get_id_for_name(self, name):
        obj = self.get_queryset().filter(name=name)
        if (obj):
            return obj
        else:
            return None

    def get_genre_of_name(self, name):
        result = []
        if (isinstance(name, list)):
            for elem in name:
                result.append(self.get_id_for_name(elem))
        else:
            result.append(self.get_id_for_name(name))
        return result


class MovieManager(models.Manager):
    """ MOVIE MANAGER """

    def get_queryset(self):
        return super().get_queryset()

    def get_last_ten(self):
        return self.get_queryset().order_by('-id')[:10]

    def get_last_twentyfive(self):
        return self.get_queryset().order_by('-id')[:25]

    def sort_by_rating(self):
        return self.get_queryset().order_by('-rating')[:10]

    def n_sort_by_rating_recom(self, pk):
        return self.get_queryset().filter(~Q(id=pk)).order_by('-rating')[:10]

    def get_poster_by_id(self, id):
        obj = self.get_queryset().get(id=id)
        return obj.get_poster()


class SerieManager(models.Manager):
    """ SERIE MANAGER """

    def get_queryset(self):
        return super().get_queryset()

    def get_last_ten(self):
        return self.get_queryset().order_by('-id')[:10]

    def get_last_twentyfive(self):
        return self.get_queryset().order_by('-id')[:25]

    def sort_by_rating(self):
        return self.get_queryset().order_by('-rating')[:10]

    def n_sort_by_rating_recom(self, pk):
        return self.get_queryset().filter(~Q(id=pk)).order_by('-rating')[:10]

    def get_poster_by_id(self, id):
        obj = self.get_queryset().get(id=id)
        return obj.get_poster()


class SportManager(models.Manager):
    """ SPORT MANAGER """

    def get_queryset(self):
        return super().get_queryset()

    def last_ten(self):
        return self.get_queryset().order_by('-id')[:10]

    def get_last_twentyfive(self):
        return self.get_queryset().order_by('-id')[:25]


class ChannelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_last_ten(self):
        return self.get_queryset().order_by('-id')[:10]

    def get_last_twentyfive(self):
        return self.get_queryset().order_by('-id')[:25]

    def sort_by_rating(self):
        return self.get_queryset().order_by('-rating')[:10]

    def n_sort_by_rating_recom(self, pk):
        return self.get_queryset().filter(~Q(id=pk)).order_by('-rating')[:10]

    def get_poster_by_id(self, id):
        obj = self.get_queryset().get(id=id)
        return obj.get_poster()


class ShowManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_last_ten(self):
        return self.get_queryset().order_by('-id')[:10]

    def get_last_twentyfive(self):
        return self.get_queryset().order_by('-id')[:25]

    def sort_by_rating(self):
        return self.get_queryset().order_by('-rating')[:10]

    def n_sort_by_rating_recom(self, pk):
        return self.get_queryset().filter(~Q(id=pk)).order_by('-rating')[:10]

    def get_poster_by_id(self, id):
        obj = self.get_queryset().get(id=id)
        return obj.get_poster()


# ------------------- MANAGERS -------------------


# +++++++++++++++++++ ADDITIONAL MODELS +++++++++++++++++++


# ////////////////MOVIE-SERIES

class Genre(models.Model):
    name = models.CharField("Название жанра", max_length=100, null=False, blank=False)
    icon = models.ImageField("Иконка жанра", upload_to='uploads/genres/icons/', null=True, blank=True)
    objects = GenreManager()

    def __str__(self):
        return self.name

    def get_icon(self):
        if not self.icon:
            return '/static/main/img/icons/popup-close.svg'
        return f"/media/{self.icon}"

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Country(models.Model):
    name = models.CharField("Название страны", max_length=100, null=False, blank=False)
    iso3 = models.CharField("ISO3", max_length=10, null=True, blank=True)
    iso3_code = models.CharField("ISO3 Code", max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"


class Language(models.Model):
    name = models.CharField("Название языка", max_length=100, null=False, blank=False)
    iso3 = models.CharField("ISO3", max_length=10, null=True, blank=True)
    iso3_code = models.CharField("ISO3 Code", max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"

class Subtitle(models.Model):
    file_name = models.CharField("Название файла", max_length=512, null=False, blank=False)
    file_extension = models.CharField("Расширение файла", max_length=100, null=False, blank=False)
    language = models.CharField("Язык", max_length=100, null=True, blank=True)


    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = "Субтитры"
        verbose_name_plural = "Субтитры"


# /////////////////////////////

# //////////////SPORT

class SportKind(models.Model):
    name = models.CharField("Название вида спорта", max_length=100, null=False, blank=False)
    icon = models.ImageField("Иконка вида спорта", upload_to='uploads/sportkinds/icons/', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_icon(self):
        if not self.icon:
            return '/static/main/img/icons/popup-close.svg'
        return f"/media/{self.icon}"

    class Meta:
        verbose_name = "Вид спорта"
        verbose_name_plural = "виды спорта"


# /////////////////////

# ///////////////SHOWS-CHANNELS

class ChannelProvider(models.Model):
    # [name, poster_url, based(тут страна в ISO3), language, genres]
    name = models.CharField("Название провайдера", max_length=100, null=True, blank=True)
    poster_url = models.URLField(verbose_name="Постер провайдера (URL)", blank=True, null=True)
    poster = models.ImageField("Постер провайдера", upload_to='uploads/series/posters/', null=True, blank=True)
    poster_ch = models.BooleanField(verbose_name="Использовать для постера URL?", default=False)
    based = models.ForeignKey(Country, verbose_name="Находиться в", on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey(Language, verbose_name="Язык провайдера", on_delete=models.SET_NULL, null=True,
                                 blank=True)
    genre = models.ManyToManyField(Genre, verbose_name="Жанры провайдера", blank=True)

    def __str__(self):
        return self.name

    def get_poster(self):
        if (self.poster_ch):
            return self.poster_url
        else:
            return f"/media/{self.poster}"

    def get_count_channels(self):
        return self.channel_set.count()

    class Meta:
        verbose_name = "Провайдер"
        verbose_name_plural = "Провайдеры"


# /////////////////////////////

# ------------------- ADDITIONAL MODELS -------------------


# +++++++++++++++++++ MAIN MODELS +++++++++++++++++++

# 128x175 , big banner: 320x179, video-preview: 171x105, search-img: 50x60
class Movie(models.Model):
    # [name, year, genres, description, imdb_id, imdb_rating, poster_url, video_url, duration, country(ISO3), language, imdb_link]
    name = models.CharField("Название фильма", max_length=100, null=True, blank=True)
    year = models.IntegerField("Год выхода фильма", default=2021, null=True, blank=True)
    genre = models.ManyToManyField(Genre, verbose_name="Жанры фильма", blank=True)
    description = models.TextField("Описание фильма", max_length=2000, blank=True)
    imdb_id = models.CharField("IMDB-id", max_length=100, null=True, blank=True, unique=True)
    imdb_rating = models.FloatField("Рейтинг фильма (IMDB)", default=0, max_length=10, blank=True, null=True)
    user_rating_all = models.IntegerField("Рейтинг фильма (польз)", default=0, null=True, blank=True)
    user_rating_q = models.IntegerField("Количество проголосовавших", default=0, null=True, blank=True)
    poster_url = models.URLField("Постер фильма (с IMDB)", blank=True, null=True)
    big_poster_url = models.URLField("Постер фильма (BigSlider)", blank=True, null=True, default='')
    video_url = models.CharField(verbose_name="Видео-файл фильма (URL-GET)", max_length=255, blank=True, null=True)
    duration = models.CharField("Длительность фильма", default="1:30", max_length=30, null=True, blank=True)
    subtitle_urls = models.TextField('Ссылки на субтитры (через зап.)', null=True, blank=True)
    date_pub = models.DateTimeField("Дата загрузки фильма", auto_now=True)
    country = models.ForeignKey(Country, verbose_name="Страна выхода фильма", on_delete=models.SET_NULL, null=True,
                                blank=True)
    language = models.ForeignKey(Language, verbose_name="Язык фильма", on_delete=models.SET_NULL, null=True,
                                 blank=True)
    imdb_link = models.URLField("Ссылка на IMDB", blank=True, null=True)
    hide_movie = models.BooleanField("Отключить показ фильма", default=False)
    watchhistoryes = GenericRelation('users.UserWatchHisory', related_query_name='watchhis')
    watchlists = GenericRelation('users.UserWatchList', related_query_name='watchlists')
    comments = GenericRelation('users.Comment', related_query_name='comments')
    watch_counter = models.PositiveIntegerField("Просмотры", default=0)
    rev_url_name = models.CharField('Имя url', max_length=255, default='movie-page')
    is_active = models.BooleanField('Активно', default=True)
    objects = MovieManager()

    def __str__(self):
        return f"Фильм - {self.name}"

    def get_poster(self):
        return self.poster_url

    def get_big_poster(self):
        if self.big_poster_url:
            return self.big_poster_url
        return self.poster_url

    def get_video(self):
        return self.video_url

    def get_name(self):
        if (len(self.name.strip()) >= 19):  # or (len(x) >= 8 for x in self.name.split(" ")):
            return (self.name[:15]).strip() + "..."
        else:
            return self.name.strip()

    def get_name_live_search(self):
        if (len(self.name.strip()) >= 25):  # or (len(x) >= 8 for x in self.name.split(" ")):
            return (self.name[:22]).strip() + "..."
        else:
            return self.name.strip()

    def get_genres(self):
        genres = []
        for i in self.genre.all():
            genres.append(i.name)
        return ', '.join(genres)

    def get_two_genres(self):
        genres = []
        for i in self.genre.all()[:2]:
            genres.append(i.name)
        return ', '.join(genres)

    def get_rating(self):
        try:
            rating = float("%.1f" % (self.user_rating_all / self.user_rating_q))
            return {
                "grade": rating,
                "based": self.user_rating_q
            }
        except ZeroDivisionError:
            return False

    def get_search_rating(self):
        try:
            return float("%.1f" % (self.user_rating_all / self.user_rating_q))
        except ZeroDivisionError:
            rating = float("%.1f" % (self.imdb_rating + 0.7))
            if rating > 10:
                rating = rating - (rating % 10)
            return rating

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieAltLang(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')
    video_url = models.CharField(verbose_name="Видео-файл фильма (URL-GET)", max_length=255, blank=True, null=True)
    language = models.ForeignKey(Language, verbose_name="Язык фильма", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Mv. ({self.movie.name})"

    class Meta:
        verbose_name = "Доп. языки фильма"
        verbose_name_plural = "Доп. языки фильмов"


class Serie(models.Model):
    name = models.CharField("Название сериала", max_length=100, null=True, blank=True)
    year = models.PositiveIntegerField("Год выхода сериала", default=2021, null=True, blank=True)
    genre = models.ManyToManyField(Genre, verbose_name="Жанры сериала", blank=True)
    description = models.TextField("Описание сериала", max_length=2000, blank=True)
    imdb_id = models.CharField("IMDB-id", max_length=100, null=True, blank=True, unique=True)
    imdb_rating = models.FloatField("Рейтинг сериала (IMDB)", blank=True, default=0, null=True)
    user_rating_all = models.IntegerField("Рейтинг сериала (польз)", default=0, null=True, blank=True)
    user_rating_q = models.IntegerField("Количество проголосовавших", default=0, null=True, blank=True)
    poster_url = models.CharField(verbose_name="Постер сериала (URL)", max_length=255, blank=True, null=True)
    big_poster_url = models.URLField("Постер сериала (BigSlider)", blank=True, null=True, default='')
    date_pub = models.DateTimeField("Дата загрузки сериала", auto_now=True)
    country = models.ForeignKey(Country, verbose_name="Страна выхода сериала", on_delete=models.SET_NULL, null=True,
                                blank=True)
    language = models.ForeignKey(Language, verbose_name="Язык сериала", on_delete=models.SET_NULL, null=True,
                                 blank=True)
    imdb_link = models.URLField("Ссылка на IMDB", blank=True, null=True)
    watch_counter = models.PositiveIntegerField("Просмотры", default=0)
    rev_url_name = models.CharField('Имя url', max_length=255, default='serie-page')
    is_active = models.BooleanField('Активно', default=True)
    objects = SerieManager()

    def __str__(self):
        return f"Сериал ({self.name})"

    def get_poster(self):
        return self.poster_url

    def get_big_poster(self):
        if self.big_poster_url:
            return self.big_poster_url
        return self.poster_url

    def get_genres(self):
        genres = []
        for i in self.genre.all():
            genres.append(i.name)
        return ', '.join(genres)

    def get_two_genres(self):
        genres = []
        for i in self.genre.all()[:2]:
            genres.append(i.name)
        return ', '.join(genres)

    def get_name(self):
        if (len(self.name.strip()) >= 19):  # or (len(x) >= 8 for x in self.name.split(" ")):
            return (self.name[:15]).strip() + "..."
        else:
            return self.name.strip()

    def get_name_live_search(self):
        if (len(self.name.strip()) >= 25):  # or (len(x) >= 8 for x in self.name.split(" ")):
            return (self.name[:22]).strip() + "..."
        else:
            return self.name.strip()

    def get_rating(self):
        try:
            rating = float("%.1f" % (self.user_rating_all / self.user_rating_q))
            return {
                "grade": rating,
                "based": self.user_rating_q
            }
        except ZeroDivisionError:
            return False

    def get_search_rating(self):
        try:
            return float("%.1f" % (self.user_rating_all / self.user_rating_q))
        except ZeroDivisionError:
            rating = float("%.1f" % (self.imdb_rating + 0.7))
            if rating > 10:
                rating = rating - (rating % 10)
            return rating

    class Meta:
        verbose_name = "Сериал"
        verbose_name_plural = "Сериалы"


class SerieSeason(models.Model):
    serie = models.ForeignKey(Serie, verbose_name="Сериал", on_delete=models.CASCADE, default=1, related_name="serii")
    season_num = models.PositiveIntegerField("Номер сезона", default=1, null=False, blank=False)

    def __str__(self):
        return f"{self.season_num} ({self.serie.name}) "

    class Meta:
        verbose_name = "Сезон сериала"
        verbose_name_plural = "Сезоны сериалов"


class SerieEpisode(models.Model):
    # [name, year, genres, description, imdb_id, imdb_rating, poster_url, country(ISO3), language, imdb_link, season_num, episode_num, episode_preview_url, episode_video_url, duration]
    episode = models.PositiveIntegerField("Номер епизода", default=1, null=False, blank=False)
    episode_name = models.CharField("Название эпизода", max_length=255, blank=True)
    episode_imdb_id = models.CharField("IMDB ID эпизода", max_length=100, blank=True)
    season = models.ForeignKey(SerieSeason, verbose_name="Сезон", on_delete=models.CASCADE, null=True,
                               related_name="seas")
    watchhistoryes = GenericRelation('users.UserWatchHisory', related_query_name='watchhis')
    watchlists = GenericRelation('users.UserWatchList', related_query_name='watchlists')
    comments = GenericRelation('users.Comment', related_query_name='comments')
    preview_url = models.CharField(verbose_name="Превью эпизода (URL)", max_length=255, blank=True, null=True)
    video_url = models.CharField(verbose_name="Видео-файл эпизода (URL-GET)", max_length=255, blank=True, null=True)
    duration = models.CharField("Длительность видео", max_length=30, null=True, blank=True)
    date_pub = models.DateTimeField("Дата загрузки епизода", auto_now=True)
    language = models.ForeignKey(Language, verbose_name="Язык эпизода", on_delete=models.SET_NULL, null=True,
                                 blank=True)
    watch_counter = models.PositiveIntegerField("Просмотры", default=0)
    subtitle_urls = models.TextField('Ссылки на субтитры (через зап.)', null=True, blank=True)
    rev_url_name = models.CharField('Имя url', max_length=255, default='serie-page')

    def __str__(self):
        return f"Ep. ({self.episode_name} | s{self.season.season_num} | e{self.episode})"

    def get_video(self):
        return self.video_url

    def get_preview(self):
        return self.preview_url

    class Meta:
        verbose_name = "Эпизод сериала"
        verbose_name_plural = "Эпизоды сериалов"


class SerieEpAltLang(models.Model):
    episode = models.ForeignKey(SerieEpisode, on_delete=models.CASCADE, verbose_name='Эпизод')
    video_url = models.CharField(verbose_name="Видео-файл эпизода (URL-GET)", max_length=255, blank=True, null=True)
    language = models.ForeignKey(Language, verbose_name="Язык эпизода", on_delete=models.SET_NULL, null=True,
                                 blank=True)


    def __str__(self):
        return f"Ep. ({self.episode.episode_name} | s{self.episode.season.season_num} | e{self.episode.episode})"
    class Meta:
        verbose_name = "Доп. языки эпизода сериала"
        verbose_name_plural = "Доп. эпизодов сериала"



class Sport(models.Model):
    # [name(кто против кого), start_date, kind, video_url(если прямая трансл. то в live_choice - 1), live_choice(1 или 0), poster_url, country, language]
    name = models.CharField("Название матча", max_length=255, null=True, blank=True)
    start = models.DateTimeField("Дата и время начала", default=now)
    kind = models.ForeignKey(SportKind, verbose_name="Вид спорта", on_delete=models.SET_NULL, null=True)
    user_rating_all = models.IntegerField("Рейтинг фильма (польз)", default=0, null=True, blank=True)
    user_rating_q = models.IntegerField("Количество проголосовавших", default=0, null=True, blank=True)
    video_url = models.CharField(verbose_name="Ссылка на видео/прямую трансляцию матча", max_length=700,
                                 blank=True,
                                 null=True)
    live_ch = models.BooleanField(verbose_name="Это прямая трансляция?", default=True)
    poster_url = models.URLField(verbose_name="Постер прямой трансляции (URL)", blank=True, null=True)
    big_poster_url = models.URLField("Постер спорт. (BigSlider)", blank=True, null=True, default='')
    watching = models.IntegerField(verbose_name="Количество зрителей/просмотров", default=0, blank=False)
    date_created = models.DateTimeField("Дата добавления", default=now)
    language = models.ForeignKey(Language, verbose_name="Язык", on_delete=models.SET_NULL, null=True,
                                 blank=True)
    watchhistoryes = GenericRelation('users.UserWatchHisory', related_query_name='watchhis')
    watchlists = GenericRelation('users.UserWatchList', related_query_name='watchlists')
    comments = GenericRelation('users.Comment', related_query_name='comments')
    rev_url_name = models.CharField('Имя url', max_length=255, default='sport-page')
    watch_counter = models.PositiveIntegerField("Просмотры", default=0)
    is_active = models.BooleanField('Активно', default=True)
    objects = SportManager()

    def __str__(self):
        return f"Спотривное событие ({self.name})"

    def get_name(self):
        if (len(self.name.strip()) >= 30):  # or (len(x) >= 8 for x in self.name.split(" ")):
            return (self.name[:30]).strip() + "..."
        else:
            return self.name.strip()

    def get_poster(self):
        if self.poster_url:
            return self.poster_url
        return ""

    def get_big_poster(self):
        if self.big_poster_url:
            return self.big_poster_url
        return self.poster_url

    def get_video(self):
        return self.video_url

    def get_date(self):
        time = datetime.now()
        if self.date_created.hour == time.hour:
            return "Added " + str(time.minute - self.date_created.minute) + " minutes ago"
        else:
            if self.date_created.day == time.day:
                return "Added " + str(time.hour - self.date_created.hour) + " hours ago"
            else:
                if self.date_created.month == time.month:
                    return "Added " + str(time.day - self.date_created.day) + " days ago"
                else:
                    if self.date_created.year == time.year:
                        return "Added " + str(time.month - self.date_created.month) + " months ago"
        return "Added " + str(self.date_created)

    def get_name_live_search(self):
        if (len(self.name.strip()) >= 25):  # or (len(x) >= 8 for x in self.name.split(" ")):
            return (self.name[:22]).strip() + "..."
        else:
            return self.name.strip()

    def get_rating(self):
        try:
            rating = float("%.1f" % (self.user_rating_all / self.user_rating_q))
            return {
                "grade": rating,
                "based": self.user_rating_q
            }
        except ZeroDivisionError:
            return False

    def get_search_rating(self):
        try:
            return float("%.1f" % (self.user_rating_all / self.user_rating_q))
        except ZeroDivisionError:
            return 5.5

    class Meta:
        verbose_name = "Спортивное событие"
        verbose_name_plural = "Спортивные события"


class Channel(models.Model):
    # [name, live_url, poster_url, country(ISO3), language, genres]
    name = models.CharField("Название канала", max_length=100, null=True, blank=True)
    provider = models.ForeignKey(ChannelProvider, on_delete=models.SET_NULL, null=True)
    user_rating_all = models.IntegerField("Рейтинг фильма (польз)", default=0, null=True, blank=True)
    user_rating_q = models.IntegerField("Количество проголосовавших", default=0, null=True, blank=True)
    get_url = models.CharField("Ссылка на трансляцию (URL-GET)", max_length=255, )
    poster_url = models.URLField(verbose_name="Постер канала (URL)", blank=True, null=True)
    big_poster_url = models.URLField("Постер фильма (BigSlider)", blank=True, null=True, default='')
    preview_url = models.URLField(verbose_name="Превью канала (URL)", blank=True, null=True)
    viewers = models.IntegerField("Количество зрителей", default=0, null=True, blank=True)
    country = models.ForeignKey(Country, verbose_name="Страна канала", on_delete=models.SET_NULL, null=True,
                                blank=True)
    language = models.ForeignKey(Language, verbose_name="Язык канала", on_delete=models.SET_NULL, null=True,
                                 blank=True)
    genre = models.ManyToManyField(Genre, verbose_name="Жанры канала", blank=True)
    comments = GenericRelation('users.Comment', related_query_name='comments')
    rev_url_name = models.CharField('Имя url', max_length=255, default='channel-page')
    watch_counter = models.PositiveIntegerField("Просмотры", default=0)
    watchlists = GenericRelation('users.UserWatchList', related_query_name='watchlists')
    is_iptv = models.BooleanField('is iptv', default=False)
    is_active = models.BooleanField('Активно', default=True)
    objects = ChannelManager()

    def __str__(self):
        return f"Канал ({self.name})"

    def get_video(self):
        return self.get_url

    def get_poster(self):
        return self.poster_url

    def get_big_poster(self):
        if self.big_poster_url:
            return self.big_poster_url
        return self.poster_url

    def get_preview(self):
        if self.preview_url == None or self.preview_url == '':
            return self.poster_url
        return self.preview_url

    def get_name_live_search(self):
        if (len(self.name.strip()) >= 25):  # or (len(x) >= 8 for x in self.name.split(" ")):
            return (self.name[:22]).strip() + "..."
        else:
            return self.name.strip()

    def get_genres(self):
        genres = []
        for i in self.genre.all():
            genres.append(i.name)
        return ', '.join(genres)

    def get_two_genres(self):
        genres = []
        for i in self.genre.all()[:2]:
            genres.append(i.name)
        return ', '.join(genres)

    def get_rating(self):
        try:
            rating = float("%.1f" % (self.user_rating_all / self.user_rating_q))
            return {
                "grade": rating,
                "based": self.user_rating_q
            }
        except ZeroDivisionError:
            return False

    def get_search_rating(self):
        try:
            return float("%.1f" % (self.user_rating_all / self.user_rating_q))
        except ZeroDivisionError:
            return 5.5

    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"


class Show(models.Model):
    name = models.CharField("Название тв-шоу", max_length=100, null=True, blank=True)
    year = models.PositiveIntegerField("Год выхода тв-шоу", default=2021, null=True, blank=True)
    genre = models.ManyToManyField(Genre, verbose_name="Жанры тв-шоу", blank=True)
    description = models.TextField("Описание тв-шоу", max_length=2000, blank=True)
    imdb_id = models.CharField("IMDB-id", max_length=100, null=True, blank=True, unique=True)
    imdb_rating = models.FloatField("Рейтинг тв-шоу (IMDB)", blank=True, default=0, null=True)
    user_rating_all = models.IntegerField("Рейтинг фильма (польз)", default=0, null=True, blank=True)
    user_rating_q = models.IntegerField("Количество проголосовавших", default=0, null=True, blank=True)
    poster_url = models.URLField(verbose_name="Постер тв-шоу (URL)", blank=True, null=True)
    big_poster_url = models.URLField("Постер фильма (BigSlider)", blank=True, null=True, default='')
    date_pub = models.DateTimeField("Дата загрузки тв-шоу", auto_now=True)
    country = models.ForeignKey(Country, verbose_name="Страна выхода тв-шоу", on_delete=models.SET_NULL, null=True,
                                blank=True)
    language = models.ForeignKey(Language, verbose_name="Язык шоу", on_delete=models.SET_NULL, null=True, blank=True)
    imdb_link = models.URLField("Ссылка на IMDB", blank=True, null=True)
    rev_url_name = models.CharField('Имя url', max_length=255, default='show-page')
    watch_counter = models.PositiveIntegerField("Просмотры", default=0)
    is_active = models.BooleanField('Активно', default=True)
    objects = ShowManager()

    def __str__(self):
        return f"ТВ-Шоу ({self.name})"

    def get_poster(self):
        return self.poster_url

    def get_big_poster(self):
        if self.big_poster_url:
            return self.big_poster_url
        return self.poster_url

    def get_genres(self):
        genres = []
        for i in self.genre.all():
            genres.append(i.name)
        return ', '.join(genres)

    def get_two_genres(self):
        genres = []
        for i in self.genre.all()[:2]:
            genres.append(i.name)
        return ', '.join(genres)

    def get_name(self):
        if (len(self.name.strip()) >= 19):  # or (len(x) >= 8 for x in self.name.split(" ")):
            return (self.name[:15]).strip() + "..."
        else:
            return self.name.strip()

    def get_name_live_search(self):
        if (len(self.name.strip()) >= 25):  # or (len(x) >= 8 for x in self.name.split(" ")):
            return (self.name[:22]).strip() + "..."
        else:
            return self.name.strip()

    def get_rating(self):
        try:
            rating = float("%.1f" % (self.user_rating_all / self.user_rating_q))
            return {
                "grade": rating,
                "based": self.user_rating_q
            }
        except ZeroDivisionError:
            return False

    def get_search_rating(self):
        try:
            return float("%.1f" % (self.user_rating_all / self.user_rating_q))
        except ZeroDivisionError:
            rating = float("%.1f" % (self.imdb_rating + 0.7))
            if rating > 10:
                rating = rating - (rating % 10)
            return rating

    class Meta:
        verbose_name = "ТВ-Шоу"
        verbose_name_plural = "ТВ-Шоу"


class ShowSeason(models.Model):
    show = models.ForeignKey(Show, verbose_name="Шоу", on_delete=models.CASCADE, default=1, related_name="shouseas")
    season_num = models.PositiveIntegerField("Номер сезона", default=1, null=False, blank=False)

    def __str__(self):
        return f"({self.show.name}) {self.season_num} сезон"

    class Meta:
        verbose_name = "Сезон ТВ-Шоу"
        verbose_name_plural = "Сезоны ТВ-Шоу"


class ShowEpisode(models.Model):
    episode = models.PositiveIntegerField("Номер епизода", default=1, null=False, blank=False)
    episode_name = models.CharField("Название эпизода", max_length=255, blank=True)
    episode_imdb_id = models.CharField("IMDB ID эпизода", max_length=100, blank=True)

    season = models.ForeignKey(ShowSeason, verbose_name="Сезон", on_delete=models.CASCADE, null=True,
                               related_name="seas")
    watchhistoryes = GenericRelation('users.UserWatchHisory', related_query_name='watchhis')
    watchlists = GenericRelation('users.UserWatchList', related_query_name='watchlists')
    comments = GenericRelation('users.Comment', related_query_name='comments')
    preview_url = models.CharField(verbose_name="Превью эпизода (URL)", max_length=255, blank=True, null=True)
    video_url = models.CharField(verbose_name="Видео-файл эпизода (URL-GET)", max_length=255, blank=True, null=True)
    duration = models.CharField("Длительность видео", max_length=30, null=True, blank=True)
    date_pub = models.DateTimeField("Дата загрузки епизода", auto_now=True)
    subtitle_urls = models.TextField('Ссылки на субтитры (через зап.)', null=True, blank=True)
    rev_url_name = models.CharField('Имя url', max_length=255, default='show-page')
    watch_counter = models.PositiveIntegerField("Просмотры", default=0)
    language = models.ForeignKey(Language, verbose_name="Язык тв-шоу", on_delete=models.SET_NULL, null=True,
                                 blank=True)

    def __str__(self):
        return f"Эпизод ({self.episode}) | сезон ({self.season}) | шоу ({self.season.show.name})"

    def get_video(self):
        return self.video_url

    def get_preview(self):
        return self.preview_url

    class Meta:
        verbose_name = "Эпизод шоу"
        verbose_name_plural = "Эпизоды шоу"


class ShowEpAltLang(models.Model):
    episode = models.ForeignKey(ShowEpisode, on_delete=models.CASCADE, verbose_name='Эпизод')
    video_url = models.CharField(verbose_name="Видео-файл эпизода (URL-GET)", max_length=255, blank=True, null=True)
    language = models.ForeignKey(Language, verbose_name="Язык эпизода", on_delete=models.SET_NULL, null=True,
                                 blank=True)

    class Meta:
        verbose_name = "Доп. языки эпизода тв-шоу"
        verbose_name_plural = "Доп. эпизодов тв-шоу"


# ------------------- MAIN MODELS -------------------


# +++++++++++++++++++ LISTS MODELS +++++++++++++++++++


class Movielist(models.Model):
    name = models.CharField("Название подборки из фильмов", max_length=100, blank=False, null=False)
    sort_method = models.TextField("Фильмы (imdb-id,id через запятую):", blank=False, default='')
    poster_url = models.URLField(verbose_name="Постер подборки (URL)", blank=True, null=True)
    hide = models.BooleanField("Скрыть подборку", default=False)

    def __str__(self):
        return f"Подборка из фильмов ({self.name})"

    def get_poster(self):
        return self.poster_url

    class Meta:
        verbose_name = "Подборки из фильмов"
        verbose_name_plural = "Подборки из фильмов"


class Serielist(models.Model):
    name = models.CharField("Название подборки из сериалов", max_length=100, blank=False, null=False)
    sort_method = models.TextField("Сериалы (imdb-id,id через запятую):", blank=False, default='')
    poster_url = models.URLField(verbose_name="Постер подборки (URL)", blank=True, null=True)
    hide = models.BooleanField("Скрыть подборку", default=False)

    def __str__(self):
        return f"Подборка из сериалов ({self.name})"

    def get_poster(self):
        return self.poster_url

    class Meta:
        verbose_name = "Подборка из сериалов"
        verbose_name_plural = "Подборки из сериалов"


class Sportlist(models.Model):
    name = models.CharField("Название подборки из спорт. событий", max_length=100, blank=False, null=False)
    sort_method = models.TextField("Спорт.соб. (id через запятую):", blank=False, default='')
    poster_url = models.URLField(verbose_name="Постер подборки (URL)", blank=True, null=True)
    hide = models.BooleanField("Скрыть подборку", default=False)

    def __str__(self):
        return f"Подборка из спорт. событий ({self.name})"

    def get_poster(self):
        return self.poster_url

    class Meta:
        verbose_name = "Подборка из спорт. событий"
        verbose_name_plural = "Подборки из спорт. событий"


class Showlist(models.Model):
    name = models.CharField("Название подборки из тв-шоу", max_length=100, blank=False, null=False)
    sort_method = models.TextField("Тв-шоу (imdb-id через запятую):", blank=False, default='')
    poster_url = models.URLField(verbose_name="Постер подборки (URL)", blank=True, null=True)
    hide = models.BooleanField("Скрыть подборку", default=False)

    def __str__(self):
        return f"Подборка из тв-шоу ({self.name})"

    def get_poster(self):
        return self.poster_url

    class Meta:
        verbose_name = "Подборка из тв-шоу"
        verbose_name_plural = "Подборки из тв-шоу"


class Channellist(models.Model):
    name = models.CharField("Название подборки из каналов", max_length=100, blank=False, null=False)
    sort_method = models.TextField("Каналы (id через запятую):", blank=False, default='')
    poster_url = models.URLField(verbose_name="Постер подборки (URL)", blank=True, null=True)
    hide = models.BooleanField("Скрыть подборку", default=False)

    def __str__(self):
        return f"Подборка из каналов ({self.name})"

    def get_poster(self):
        return self.poster_url

    class Meta:
        verbose_name = "Подборка из каналов"
        verbose_name_plural = "Подборки из каналов"


# ------------------- LISTS MODELS -------------------


# +++++++++++++++++++ SETTINGS MODELS +++++++++++++++++++


class Component(models.Model):
    handler_choices = [
        ("Models", (
            ("1", "Movie"),
            ("2", "Serie"),
            ("3", "Sport"),
            ("4", "ChannelProvider"),
            ("5", "Channel"),
            ("6", "Show"),
        )),
        ("Models-Lists", (
            ("7", "Movie-toplists"),
            ("8", "Serie-toplists"),
            ("9", "Sport-toplists"),
            ("10", "Show-toplists"),
            ("11", "Channel-toplists"),
        ))
    ]
    name = models.CharField("Название шаблона", max_length=100, null=False, blank=False)
    name_on_page = models.CharField("Название блока на странице*", max_length=100, null=True, blank=True,
                                    default="PAGE BLOCK")
    handler = models.CharField("Обработчик сортировки**", choices=handler_choices, max_length=2, null=True, blank=True)
    # c_num = models.IntegerField("Внутренний номер компонента", default=0, unique=True, null=False, blank=False)
    path = models.TextField("Путь к компоненту", max_length=1024, null=False, blank=False)
    sort_method = models.TextField("Сортировка (imdb-id,id через запятую):", blank=False)

    def __str__(self):
        return f"Компонент ({self.name})"

    class Meta:
        verbose_name = "Компонент для страницы"
        verbose_name_plural = "Компоненты для страниц"


class Page(models.Model):
    name = models.CharField("Название страницы", max_length=100, null=False, blank=False)
    p_num = models.IntegerField("Внутренний номер компонента", default=0, unique=True, null=False, blank=False)
    title = models.CharField("Title страницы", max_length=150, null=True, blank=True)
    element1 = models.ForeignKey(Component, verbose_name="Компонент №1", on_delete=models.SET_NULL, null=True,
                                 related_name="element_first", blank=True)
    element2 = models.ForeignKey(Component, verbose_name="Компонент №2", on_delete=models.SET_NULL, null=True,
                                 related_name="element_two", blank=True)
    element3 = models.ForeignKey(Component, verbose_name="Компонент №3", on_delete=models.SET_NULL, null=True,
                                 related_name="element_thrid", blank=True)
    element4 = models.ForeignKey(Component, verbose_name="Компонент №4", on_delete=models.SET_NULL, null=True,
                                 related_name="element_four", blank=True)
    element5 = models.ForeignKey(Component, verbose_name="Компонент №5", on_delete=models.SET_NULL, null=True,
                                 related_name="element_five", blank=True)
    element6 = models.ForeignKey(Component, verbose_name="Компонент №6", on_delete=models.SET_NULL, null=True,
                                 related_name="element_six", blank=True)
    element7 = models.ForeignKey(Component, verbose_name="Компонент №7", on_delete=models.SET_NULL, null=True,
                                 related_name="element_seven", blank=True)
    element8 = models.ForeignKey(Component, verbose_name="Компонент №8", on_delete=models.SET_NULL, null=True,
                                 related_name="element_eight", blank=True)
    element9 = models.ForeignKey(Component, verbose_name="Компонент №9", on_delete=models.SET_NULL, null=True,
                                 related_name="element_nine", blank=True)
    element10 = models.ForeignKey(Component, verbose_name="Компонент №10", blank=True, on_delete=models.SET_NULL,
                                  null=True,
                                  related_name="element_ten")

    def __str__(self):
        return f"Страница ({self.name})"

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"


# ------------------- SETTINGS MODELS -------------------


# +++++++++++++++++++ ADS MODELS +++++++++++++++++++

class Adbanner(models.Model):
    name = models.CharField("Название банера", max_length=100, null=True, blank=True)
    template = models.CharField("Шаблон банера*", max_length=100, null=True, blank=True)
    links = models.TextField('Ссылки для перехода (через зап.)', null=True, blank=True)
    banner_url = models.URLField(verbose_name="Ссылка на изображение", blank=True, null=True)
    events = GenericRelation('analytics.BannerAnalytics', related_query_name='events')

    def __str__(self):
        return f"Баннер ({self.name})"

    def get_banner(self):
        return self.banner_url

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"


class AdVideo(models.Model):
    name = models.CharField("Название видео-ролика", max_length=255)
    video_url = models.CharField(verbose_name="Видео-файл ролика (URL-GET)", max_length=255, blank=True, null=True)

    def get_video(self):
        return self.video_url

    def get_type(self):
        return "r"

    def __str__(self):
        return f"Видео-ролик ({self.name})"

    class Meta:
        verbose_name = "Видео-ролик для баннера"
        verbose_name_plural = "Видео-ролики для баннеров"


class AdVideoBanner(models.Model):
    b_id = models.IntegerField("Номер банера (сист)", unique=True)
    name = models.CharField("Название банера", max_length=255)
    video = models.ForeignKey(AdVideo, on_delete=models.SET_NULL, null=True)
    links = models.TextField('Ссылки для перехода (через зап.)', null=True, blank=True)
    time_to_skip = models.PositiveIntegerField("Время до показа Skip", default=5000)
    pixel = models.CharField('Ссылка на tracking - pixel', max_length=255, blank=True)
    events = GenericRelation('analytics.BannerAnalytics', related_query_name='events')

    def __str__(self):
        return f"Видео-баннер ({self.name})"

    class Meta:
        verbose_name = "Видео-баннер"
        verbose_name_plural = "Видео-баннеры"


class AdVideoMidroll(models.Model):
    b_id = models.IntegerField("Номер мидролла (сист)", unique=True)
    name = models.CharField("Название мидролла", max_length=255)
    video = models.ForeignKey(AdVideo, on_delete=models.SET_NULL, null=True)
    links = models.TextField('Ссылки для перехода (через зап.)', null=True, blank=True)
    time_to_skip = models.PositiveIntegerField("Время до показа Skip", default=5)
    timings = models.CharField("Тайминги показа мидролла в секундах (нап.: 10,20,160)", default="50", max_length=255)
    pixel = models.CharField('Ссылка на tracking - pixel', max_length=255, blank=True)
    events = GenericRelation('analytics.BannerAnalytics', related_query_name='events')

    def __str__(self):
        return f"Видео-баннер ({self.name})"

    class Meta:
        verbose_name = "Видео-мидролл"
        verbose_name_plural = "Видео-мидроллы"


# ------------------- ADS MODELS -------------------
class Setting(models.Model):
    t_id = models.PositiveIntegerField("Внутренний номер", default=1, unique=True)
    type = models.CharField("Тип", max_length=255, blank=False, unique=True)
    value = models.CharField("Значение", max_length=512, blank=True, unique=False)

    def __str__(self):
        return f"Параметр {self.type}"

    class Meta:
        verbose_name = "Параметр"
        verbose_name_plural = "Параметры"


class Popup(models.Model):
    name = models.CharField("Название попапа", max_length=255)
    group = models.ForeignKey('users.UserGroup', verbose_name="Группа пользователей", null=True,
                              on_delete=models.SET_NULL, related_name='popup')
    template = models.CharField('Шаблон попапа', max_length=512)
    show_times = models.PositiveIntegerField("Количество показов", default=1)
    load_time = models.PositiveIntegerField("Время после загрузки страницы в секундах", default=5)
    active = models.BooleanField("Активность", default=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Попап"
        verbose_name_plural = "Попапы"
