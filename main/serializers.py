from rest_framework import serializers
from main.models import (
    Genre, Country, Language, SerieSeason,
    SportKind,
    ChannelProvider,
    Movie, Serie, SerieEpisode, Sport, Channel, Show, ShowSeason, ShowEpisode,
    Movielist, Serielist, Sportlist, Showlist,
    Component, Page,
    Adbanner
)

class MovieLiveSearchSerializer(serializers.ModelSerializer):
    poster = serializers.CharField(source='get_poster')
    name = serializers.CharField(source='get_name_live_search')
    genres = serializers.CharField(source='get_two_genres', read_only=True)
    rating = serializers.FloatField(source='get_search_rating')
    class Meta:
        model = Movie
        fields = ('id','name','year','genres','poster','rating')

class SerieLiveSearchSerializer(serializers.ModelSerializer):
    poster = serializers.CharField(source='get_poster')
    name = serializers.CharField(source='get_name_live_search')
    genres = serializers.CharField(source='get_two_genres', read_only=True)
    rating = serializers.FloatField(source='get_search_rating')
    class Meta:
        model = Serie
        fields = ('id','name','year','genres','poster','rating')

class SportLiveSearchSerializer(serializers.ModelSerializer):
    poster = serializers.CharField(source='get_poster')
    # name = serializers.CharField(source='name')
    year = serializers.CharField(source='kind.name', read_only=True)
    rating = serializers.FloatField(source='get_search_rating')
    class Meta:
        model = Sport
        fields = ('id','name','year','poster','rating')

class ChannelLiveSearchSerializer(serializers.ModelSerializer):
    poster = serializers.CharField(source='get_poster')
    name = serializers.CharField(source='get_name_live_search')
    genres = serializers.CharField(source='get_two_genres', read_only=True)
    rating = serializers.FloatField(source='get_search_rating')
    class Meta:
        model = Channel
        fields = ('id','name','genres','poster','rating')

class ShowLiveSearchSerializer(serializers.ModelSerializer):
    poster = serializers.CharField(source='get_poster')
    name = serializers.CharField(source='get_name_live_search')
    genres = serializers.CharField(source='get_two_genres', read_only=True)
    rating = serializers.FloatField(source='get_search_rating')
    class Meta:
        model = Show
        fields = ('id','name','year','genres','poster','rating')

class GenreFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')

class CountryFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name')

class LanguageFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name')