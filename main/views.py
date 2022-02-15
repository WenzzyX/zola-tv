from json import dumps
from django.http import HttpResponseNotFound
from django.shortcuts import HttpResponse, Http404, render, resolve_url
from django.views.generic import TemplateView, DetailView, View
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.utils.translation import gettext_noop
from django.conf import settings
from django.db.models import Q
from users.models import UserGroup
from analytics.models import FirstAnalytics
from django.template.loader import render_to_string
from django.utils.timezone import now
from datetime import datetime

from main.models import (
    Genre, Country, Language, SerieSeason,Subtitle,
    SportKind,
    ChannelProvider,
    Movie, Serie, SerieEpisode, Sport, Channel, Show, ShowSeason, ShowEpisode,
    Component, Page,
    Movielist, Serielist, Sportlist, Showlist,
    Adbanner, AdVideoBanner, MovieAltLang, SerieEpAltLang, Channellist, AdVideoMidroll, Setting, Popup
)
from main.serializers import (
    MovieLiveSearchSerializer,
    SerieLiveSearchSerializer,
    SportLiveSearchSerializer,
    ChannelLiveSearchSerializer,
    ShowLiveSearchSerializer,
    GenreFilterSerializer,
    CountryFilterSerializer,
    LanguageFilterSerializer,
    SubtitleLiveSearchSerializer
)
from analytics.utils.watch_analytics import add_view
from users.models import UserProfile, Subscription, AppRating
from main.utils.UserLists import (add_model_to_history, add_model_to_watchlist, get_object_in_watchlist,
                                  save_feedback_from_user, remove_from_history_model)
from main.utils.UserSubcription import get_subscriptions_for_user
from main.utils.UserComments import save_comment_for_model, set_like_for_comment
from main.utils.UserRating import set_rating_for_model, get_rating_for_ct_model
from main.utils.UserRefLinks import create_share_url, click_ref_link, add_download_to_url
from main.utils.UserRecovery import check_code, check_recovery_sended, send_code, delete_code, check_seconds


class PnfView(TemplateView):
    template_name = "main/pages/wrongUrl.html"

    def get_context_data(self, **kwargs):
        kwargs = super(PnfView, self).get_context_data(**kwargs)
        # kwargs.update({
        #     "page": Page.objects.get(p_num=page_num)
        # })
        return kwargs


class MainView(TemplateView):
    template_name = "main/pages/main.html"

    def get_context_data(self, **kwargs):
        kwargs = super(MainView, self).get_context_data(**kwargs)
        page_num = 1
        url = self.request.build_absolute_uri()
        click_ref_link(url)
        kwargs.update({
            "page": Page.objects.get(p_num=page_num)
        })
        return kwargs


class SportView(TemplateView):
    template_name = "main/pages/sport.html"

    # def get(self, request, *args, **kwargs):
    #     return redirect('work-in-progress-page')
    def get_context_data(self, **kwargs):
        kwargs = super(SportView, self).get_context_data(**kwargs)

        page_num = 2
        page_num_second = 12
        kwargs.update({
            "page_sport": Page.objects.get(p_num=page_num),
            "page_matches": Page.objects.get(p_num=page_num_second),
            "genres": SportKind.objects.all(),
            "languages": Language.objects.all(),
            "title": "Sports"
        })
        return kwargs


class MoviesSeriesView(TemplateView):
    template_name = "main/pages/movies-series.html"

    def get_context_data(self, **kwargs):
        kwargs = super(MoviesSeriesView, self).get_context_data(**kwargs)
        page_num = 3
        page_num_second = 4
        kwargs.update({
            "page_movies": Page.objects.get(p_num=page_num),
            "page_series": Page.objects.get(p_num=page_num_second)
        })
        return kwargs


class ShowsChannelsView(TemplateView):
    template_name = "main/pages/shows-channels.html"

    def get_context_data(self, **kwargs):
        kwargs = super(ShowsChannelsView, self).get_context_data(**kwargs)
        page_num = 5
        page_num_second = 6
        kwargs.update({
            "page_shows": Page.objects.get(p_num=page_num),
            "page_channels": Page.objects.get(p_num=page_num_second),
            "genres": Genre.objects.all(),
            "languages": Language.objects.all()
        })
        return kwargs


class LiveSearchView(View):
    def post(self, request):
        return_count = 25
        try:
            search_query, search_tab = (request.POST['q'], int(request.POST['tab']))
            result_dict = {
                search_tab == 1: dumps(
                    MovieLiveSearchSerializer(
                        Movie.objects.filter(name__icontains=search_query, is_active=True)[:return_count],
                        many=True).data),
                search_tab == 2: dumps(
                    SerieLiveSearchSerializer(
                        Serie.objects.filter(name__icontains=search_query, is_active=True)[:return_count],
                        many=True).data),
                search_tab == 3: dumps(SportLiveSearchSerializer(
                    Sport.objects.filter(name__icontains=search_query, live_ch=False)[:return_count], many=True).data),
                search_tab == 4: dumps(
                    ChannelLiveSearchSerializer(
                        Channel.objects.filter(name__icontains=search_query, is_active=True)[:return_count],
                        many=True).data),
                search_tab == 5: dumps(
                    ShowLiveSearchSerializer(
                        Show.objects.filter(name__icontains=search_query, is_active=True)[:return_count],
                        many=True).data),
            }[True]
            return HttpResponse(dumps(result_dict, ensure_ascii=False), content_type="application/json; charset=utf-8")
        except KeyError:
            return HttpResponseNotFound()


class FilterView(TemplateView):
    template_name = "main/pages/filter.html"

    def get_context_data(self, **kwargs):
        kwargs = super(FilterView, self).get_context_data(**kwargs)
        kwargs.update({
            "popup_models": {
                "id": 1,
                "name": "TYPE",
                "name_plural": "TYPES"
            },
            "popup_genres": {
                "id": 2,
                "name": "GENRE",
                "name_plural": "TYPES"
            },
            "popup_countries": {
                "id": 3,
                "name": "COUNTRY",
                "name_plural": "COUNTRIES"
            },
            "popup_languages": {
                "id": 4,
                "name": "LANGUAGE",
                "name_plural": "LANGUAGES"
            },
            "title": "Filter"
        })
        return kwargs


class FilterPopupsView(View):
    def post(self, request):
        # # return_count = 25
        try:
            search_query, search_id = (request.POST['q'], int(request.POST['id']))
            result_dict = {
                search_id == 1: dumps([
                    {
                        "id": 1,
                        "name": "Movies"
                    },
                    {
                        "id": 2,
                        "name": "Series"
                    },
                    {
                        "id": 3,
                        "name": "Sports"
                    },
                    {
                        "id": 4,
                        "name": "ChannelProviders"
                    },
                    {
                        "id": 5,
                        "name": "Channels"
                    },
                    {
                        "id": 6,
                        "name": "Tv-shows"
                    },

                ]),
                search_id == 2: dumps(
                    GenreFilterSerializer(Genre.objects.filter(name__contains=search_query), many=True).data),
                search_id == 3: dumps(
                    CountryFilterSerializer(Country.objects.filter(name__contains=search_query), many=True).data),
                search_id == 4: dumps(
                    LanguageFilterSerializer(Language.objects.filter(name__contains=search_query), many=True).data),
            }[True]
            return HttpResponse(dumps(result_dict, ensure_ascii=False), content_type="application/json; charset=utf-8")
        except KeyError:
            return HttpResponseNotFound()


class FilterResultsView(TemplateView):
    template_name = "main/pages/filter-results.html"
    title_page = "Filter results"
    return_count = 50

    def retint(self, listarg):
        for i in range(len(listarg)):
            listarg[i] = int(listarg[i])
        return listarg

    def checkofnull(self, nullor):
        if (0 in nullor):
            return False
        else:
            return True

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        finalDict = []
        model = int(request.POST['1'])
        genres = set(self.retint(list(request.POST['2'].split(","))))
        countries = set(self.retint(list(request.POST['3'].split(","))))
        languages = set(self.retint(list(request.POST['4'].split(","))))
        years = set(self.retint(list(request.POST['5'].split(","))))
        ratings = set(self.retint(list(request.POST['6'].split(","))))
        presport = request.POST.get('7') or False
        sport_kinds = {0}
        if presport:
            sport_kinds = set(self.retint(list(presport.split(","))))
        card_url = "movie-page"
        if ((model == 1 and not self.checkofnull(genres) and not self.checkofnull(countries) and not self.checkofnull(
                languages))):
            finalDict = Movie.objects.all().order_by('-id')[:self.return_count]
        else:
            if model == 1:
                card_url = "movie-page"
                filall = {}
                if (self.checkofnull(genres)):
                    filall["genre__id__in"] = genres
                if (self.checkofnull(countries)):
                    filall["country__id__in"] = countries
                if (self.checkofnull(languages)):
                    filall["language__id__in"] = languages
                if (self.checkofnull(years)):
                    filall["year__range"] = years
                if (self.checkofnull(ratings)):
                    filall["imdb_rating__range"] = ratings
                finalDict = Movie.objects.filter(**filall)
            if model == 2:
                card_url = "serie-page"
                filall = {}
                if (self.checkofnull(genres)):
                    filall["genre__id__in"] = genres
                if (self.checkofnull(countries)):
                    filall["country__id__in"] = countries
                if (self.checkofnull(languages)):
                    filall["language__id__in"] = languages
                if (self.checkofnull(years)):
                    filall["year__range"] = years
                if (self.checkofnull(ratings)):
                    filall["imdb_rating__range"] = ratings
                finalDict = Serie.objects.filter(**filall)
            if model == 3:
                card_url = "sport-page"
                filall = {}
                if (self.checkofnull(countries)):
                    filall["country__id__in"] = countries
                if (self.checkofnull(languages)):
                    filall["language__id__in"] = languages
                if (self.checkofnull(sport_kinds)):
                    filall["kind__id__in"] = sport_kinds
                finalDict = Sport.objects.filter(**filall)
            if model == 4:
                card_url = "provider-page"
                filall = {}
                if (self.checkofnull(genres)):
                    filall["genre__id__in"] = genres
                if (self.checkofnull(countries)):
                    filall["based__id__in"] = countries
                if (self.checkofnull(languages)):
                    filall["language__id__in"] = languages
                finalDict = ChannelProvider.objects.filter(**filall)
            if model == 5:
                card_url = "channel-page"
                filall = {}
                if (self.checkofnull(genres)):
                    filall["genre__id__in"] = genres
                if (self.checkofnull(countries)):
                    filall["country__id__in"] = countries
                if (self.checkofnull(languages)):
                    filall["language__id__in"] = languages
                finalDict = Channel.objects.filter(**filall)
            if model == 6:
                card_url = "show-page"
                filall = {}
                if (self.checkofnull(genres)):
                    filall["genre__id__in"] = genres
                if (self.checkofnull(countries)):
                    filall["country__id__in"] = countries
                if (self.checkofnull(languages)):
                    filall["language__id__in"] = languages
                if (self.checkofnull(years)):
                    filall["year__range"] = years
                if (self.checkofnull(ratings)):
                    filall["imdb_rating__range"] = ratings
                finalDict = Show.objects.filter(**filall)
        context.update({
            "elements": finalDict,
            "modelid": model,
            "url": card_url,
            "title": self.title_page
        })
        return super(FilterResultsView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        kwargs = super(FilterResultsView, self).get_context_data(**kwargs)
        movies = Movie.objects.filter(is_active=True)[:self.return_count]
        card_url = "movie-page"
        kwargs.update({
            "elements": movies,
            "model": 1,
            "url": card_url,
            "title": self.title_page
        })
        return kwargs


class MovieDetailView(DetailView):
    template_name = "main/pages/detail/MovieDetail.html"
    model = Movie
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        kwargs = super(MovieDetailView, self).get_context_data(**kwargs)
        this_movie = kwargs.get('movie')
        add_view(this_movie)
        page_num = 7

        if not self.request.user.is_anonymous:
            add_model_to_history(self.request.user, this_movie)
            kwargs.update({
                "add_watchlist": get_object_in_watchlist(self.request.user, this_movie)
            })
        ads_num = 1
        try:
            kwargs.update({
                "advideo": AdVideoBanner.objects.get(b_id=ads_num)
            })
        except AdVideoBanner.DoesNotExist:
            pass

        midroll_num = 1
        try:
            kwargs.update({
                "midroll": AdVideoMidroll.objects.get(b_id=midroll_num)
            })
        except AdVideoMidroll.DoesNotExist:
            pass
        altLangs = MovieAltLang.objects.filter(movie=this_movie)
        vurl = ['{' + str(this_movie.language) + '}' + str(this_movie.get_video())]
        if altLangs:
            for altlang in altLangs:
                vurl.append('{' + str(altlang.language) + '}' + str(altlang.video_url))
        vurl = (';'.join(vurl)).replace('\"', '') + ';'
        url = self.request.build_absolute_uri()
        click_ref_link(url)
        kwargs.update({
            "page": Page.objects.get(p_num=page_num),
            "vurl": vurl,
            "obj_title": gettext_noop("movie")
        })
        return kwargs


class SerieDetailView(TemplateView):
    template_name = "main/pages/detail/SerieDetail.html"

    def get_context_data(self, **kwargs):
        kwargs = super(SerieDetailView, self).get_context_data(**kwargs)
        page_num = 8
        pk = kwargs.get('pk')
        serie = Serie.objects.get(id=pk)
        if (self.request.GET.get('season') and self.request.GET.get('episode')):
            season_num, episode_num = self.request.GET.get('season'), self.request.GET.get('episode')
            season = SerieSeason.objects.get(serie=serie, season_num=season_num)
            episode = season.seas.get(episode=episode_num)
        else:
            season = SerieSeason.objects.filter(serie=serie).first()
            episode = season.seas.first()

        try:
            page = Page.objects.get(p_num=page_num)
            if not self.request.user.is_anonymous:
                add_model_to_history(self.request.user, episode)
            all_seasons = SerieSeason.objects.filter(serie=serie)
            all_episodes = season.seas.all().order_by('-episode')
            count_of_episodes = 0
            for ser in serie.serii.all():
                for ep in ser.seas.all():
                    count_of_episodes += 1

        except (Serie.DoesNotExist, SerieSeason.DoesNotExist, SerieEpisode.DoesNotExist, Page.DoesNotExist):
            raise Http404("Serie not found")
        ads_num = 1
        try:
            kwargs.update({
                "advideo": AdVideoBanner.objects.get(b_id=ads_num)
            })
        except AdVideoBanner.DoesNotExist:
            pass
        midroll_num = 1
        try:
            kwargs.update({
                "midroll": AdVideoMidroll.objects.get(b_id=midroll_num)
            })
        except AdVideoMidroll.DoesNotExist:
            pass
        altLangs = SerieEpAltLang.objects.filter(episode=episode)
        vurl = ['{' + str(episode.language) + '}' + str(episode.get_video())]
        if altLangs:
            for altlang in altLangs:
                vurl.append('{' + str(altlang.language) + '}' + str(altlang.video_url))
        vurl = (';'.join(vurl)).replace('\"', '') + ';'
        url = self.request.build_absolute_uri()
        click_ref_link(url)
        add_view(episode)
        add_view(serie)
        kwargs.update({
            "page": page,
            "serie": serie,
            "season": season,
            "episode": episode,
            "all_seasons": all_seasons,
            "all_episodes": all_episodes,
            "vurl": vurl,
            "episodes_count": count_of_episodes,
            "seasons_count": all_seasons.count(),
            "obj_title": gettext_noop("serie")
        })
        return kwargs


class ShowDetailView(TemplateView):
    template_name = "main/pages/detail/ShowDetail.html"

    def get_context_data(self, **kwargs):
        kwargs = super(ShowDetailView, self).get_context_data(**kwargs)
        page_num = 9
        pk = kwargs.get('pk')
        if (self.request.GET.get('season') and self.request.GET.get('episode')):
            season_num, episode_num = self.request.GET.get('season'), self.request.GET.get('episode')
        else:
            season_num, episode_num = 1, 1

        try:
            page = Page.objects.get(p_num=page_num)
            show = Show.objects.get(id=pk)
            season = ShowSeason.objects.get(show=show, season_num=season_num)
            episode = season.seas.get(episode=episode_num)
            if not self.request.user.is_anonymous:
                add_model_to_history(self.request.user, episode)
            all_seasons = ShowSeason.objects.filter(show=show)
            all_episodes = season.seas.all()
            count_of_episodes = 0
            for ser in show.shouseas.all():
                for ep in ser.seas.all():
                    count_of_episodes += 1

        except (Show.DoesNotExist, ShowSeason.DoesNotExist, ShowEpisode.DoesNotExist, Page.DoesNotExist):
            raise Http404("Show not found")

        ads_num = 1
        try:
            kwargs.update({
                "advideo": AdVideoBanner.objects.get(b_id=ads_num)
            })
        except AdVideoBanner.DoesNotExist:
            pass
        midroll_num = 1
        try:
            kwargs.update({
                "midroll": AdVideoMidroll.objects.get(b_id=midroll_num)
            })
        except AdVideoMidroll.DoesNotExist:
            pass
        altLangs = SerieEpAltLang.objects.filter(episode=episode)
        vurl = ['{' + str(episode.language) + '}' + str(episode.get_video())]
        if altLangs:
            for altlang in altLangs:
                vurl.append('{' + str(altlang.language) + '}' + str(altlang.video_url))
        vurl = (';'.join(vurl)).replace('\"', '') + ';'
        url = self.request.build_absolute_uri()
        click_ref_link(url)
        add_view(show)
        add_view(episode)
        kwargs.update({
            "page": page,
            "serie": show,
            "season": season,
            "episode": episode,
            "all_seasons": all_seasons,
            "all_episodes": all_episodes,
            "vurl": vurl,
            "episodes_count": count_of_episodes,
            "seasons_count": all_seasons.count(),
            "obj_title": gettext_noop("show")
        })
        return kwargs


class SportDetailView(TemplateView):
    template_name = "main/pages/detail/SportDetail.html"

    def get_context_data(self, **kwargs):
        kwargs = super(SportDetailView, self).get_context_data(**kwargs)
        page_num = 10
        pk = kwargs.get('pk')
        try:
            page = Page.objects.get(p_num=page_num)
            sport = Sport.objects.get(id=pk)
            if not self.request.user.is_anonymous:
                add_model_to_history(self.request.user, sport)

        except (Sport.DoesNotExist, Page.DoesNotExist):
            raise Http404("Sport not found")
        ads_num = 1
        try:
            kwargs.update({
                "advideo": AdVideoBanner.objects.get(b_id=ads_num)
            })
        except AdVideoBanner.DoesNotExist:
            pass
        midroll_num = 1
        try:
            kwargs.update({
                "midroll": AdVideoMidroll.objects.get(b_id=midroll_num)
            })
        except AdVideoMidroll.DoesNotExist:
            pass

        url = self.request.build_absolute_uri()
        click_ref_link(url)
        add_view(sport)
        kwargs.update({
            "page": page,
            "sport": sport,
        })
        return kwargs


class ChannelDetailView(TemplateView):
    template_name = "main/pages/detail/ChannelDetail.html"

    def get_context_data(self, **kwargs):
        kwargs = super(ChannelDetailView, self).get_context_data(**kwargs)
        page_num = 11
        pk = kwargs.get('pk')
        try:
            page = Page.objects.get(p_num=page_num)
            channel = Channel.objects.get(id=pk)

        except (Channel.DoesNotExist, Page.DoesNotExist):
            raise Http404("Channel not found")

        ads_num = 1
        try:
            kwargs.update({
                "advideo": AdVideoBanner.objects.get(b_id=ads_num)
            })
        except AdVideoBanner.DoesNotExist:
            pass

        midroll_num = 1
        try:
            kwargs.update({
                "midroll": AdVideoMidroll.objects.get(b_id=midroll_num)
            })
        except AdVideoMidroll.DoesNotExist:
            pass
        url = self.request.build_absolute_uri()
        click_ref_link(url)
        add_view(channel)
        kwargs.update({
            "page": page,
            "channel": channel,
            "obj_title": gettext_noop("channel")
        })
        return kwargs


class ChannelProviderListView(TemplateView):
    template_name = "main/pages/ChannelProviderList.html"

    def get_context_data(self, **kwargs):
        kwargs = super(ChannelProviderListView, self).get_context_data(**kwargs)
        pk = kwargs.get('pk')
        try:
            provider = ChannelProvider.objects.get(id=pk)
        except (ChannelProvider.DoesNotExist):
            raise Http404("ChannelProvider not found")

        kwargs.update({
            "provider": provider,
        })
        return kwargs


class CompilationsListView(TemplateView):
    template_name = "main/pages/ComponentList.html"

    def get_context_data(self, **kwargs):
        kwargs = super(CompilationsListView, self).get_context_data(**kwargs)
        pk = kwargs.get('pk')
        try:
            component = Component.objects.get(id=pk)
        except (Component.DoesNotExist):
            raise Http404("Compilation not found")

        kwargs.update({
            "component": component
        })
        return kwargs


class MovieCompilationListView(TemplateView):
    template_name = "main/pages/MovieCompilationList.html"

    def get_context_data(self, **kwargs):
        kwargs = super(MovieCompilationListView, self).get_context_data(**kwargs)
        pk = kwargs.get('pk')
        try:
            list = Movielist.objects.get(id=pk)
        except (Movielist.DoesNotExist):
            raise Http404("Compilation not found")

        kwargs.update({
            "list": list
        })
        return kwargs


class SerieCompilationListView(TemplateView):
    template_name = "main/pages/SerieCompilationList.html"

    def get_context_data(self, **kwargs):
        kwargs = super(SerieCompilationListView, self).get_context_data(**kwargs)
        pk = kwargs.get('pk')
        try:
            list = Serielist.objects.get(id=pk)
        except (Serielist.DoesNotExist):
            raise Http404("Compilation not found")

        kwargs.update({
            "list": list
        })
        return kwargs


class SportCompilationListView(TemplateView):
    template_name = "main/pages/SportCompilationList.html"

    def get_context_data(self, **kwargs):
        kwargs = super(SportCompilationListView, self).get_context_data(**kwargs)
        pk = kwargs.get('pk')
        try:
            list = Sportlist.objects.get(id=pk)
        except (Sportlist.DoesNotExist):
            raise Http404("Compilation not found")

        kwargs.update({
            "list": list
        })
        return kwargs


class ShowCompilationListView(TemplateView):
    template_name = "main/pages/ShowCompilationList.html"

    def get_context_data(self, **kwargs):
        kwargs = super(ShowCompilationListView, self).get_context_data(**kwargs)
        pk = kwargs.get('pk')
        try:
            list = Showlist.objects.get(id=pk)
        except (Showlist.DoesNotExist):
            raise Http404("Compilation not found")

        kwargs.update({
            "list": list
        })
        return kwargs


class ChannelCompilationListView(TemplateView):
    template_name = "main/pages/ChannelCompilationList.html"

    def get_context_data(self, **kwargs):
        kwargs = super(ChannelCompilationListView, self).get_context_data(**kwargs)
        pk = kwargs.get('pk')
        try:
            list = Channellist.objects.get(id=pk)
        except (Channellist.DoesNotExist):
            raise Http404("Compilation not found")

        kwargs.update({
            "list": list
        })
        return kwargs


class ProfileView(TemplateView):
    template_name = "main/pages/profile.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context.update({
            "title": "Profile page"
        })
        return redirect('main_page')
        if not request.user.is_anonymous:
            if not request.user.is_activated:
                return redirect('register-code-verificarion')

            if request.user.user_profile.all():
                from datetime import timedelta
                from datetime import datetime
                adf_time = timedelta(minutes=request.user.user_profile.first().ad_free_time)
                context['ad_free_time'] = adf_time
                return self.render_to_response(context)
            else:
                return redirect('profile-creation')
        return self.render_to_response(context)


class RegisterView(TemplateView):
    template_name = "main/pages/auth/register/register.html"

    def get(self, request, *args, **kwargs):
        # if not settings.ITS_APP:
        #     return redirect('app-download-page')
        context = self.get_context_data(**kwargs)
        context.update({
            "title": "Register page"
        })
        return redirect('main_page')
        if request.user.is_anonymous:
            return self.render_to_response(context)
        elif not request.user.is_activated:
            return redirect('register-code-verificarion')
        return redirect('profile-page')


class RegisterFormView(TemplateView):
    template_name = "main/pages/auth/register/registerForm.html"

    def get(self, request, *args, **kwargs):
        # if not settings.ITS_APP:
        #     return redirect('app-download-page')
        context = self.get_context_data(**kwargs)
        context['title'] = 'Register page'
        return redirect('main_page')
        if request.user.is_anonymous:
            return self.render_to_response(context)
        elif request.user.is_activated:
            return redirect('profile-page')
        return redirect('register-code-verificarion')

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['title'] = 'Register page'
        user = get_user_model()
        email = request.POST.get('email').lower() or ''
        phone = request.POST.get('phone') or ''
        password = request.POST.get('password') or ''
        ip = request.META.get('REMOTE_ADDR')
        if phone != '':
            us = user.objects.get_user_by_phone(phone)
        elif email != '':
            us = user.objects.get_user_by_email(email)
        if us:
            context['errors'] = ['This phone or email is registered.']
            return self.render_to_response(context)
        try:
            if user.objects.create_user_out(email=email, phone=phone, password=password, ip=ip):
                user = authenticate(username=email or phone, password=password)
                login(request, user)
            else:
                return redirect('register-form-page')
        except:
            context['errors'] = ['Can\'t create user.']
            return self.render_to_response(context)

        return redirect('register-code-verificarion')


# pr_view -> send_post_phone(send code) -> render next step (code input) -> send_post (phone, code) .(handle errors)
# -> render password input .(handle pass validator) -> send_post (phone. code, password)

class PhoneRecoverPassView(TemplateView):
    template_name = "main/pages/auth/recoverPass/phoneRecover.html"

    def get(self, request, *args, **kwargs):
        # if not settings.ITS_APP:
        #     return redirect('app-download-page')
        context = self.get_context_data(**kwargs)
        context['title'] = "Password recovery"
        return redirect('main_page')
        if not request.user.is_anonymous:
            return redirect('profile-page')
        return self.render_to_response(context)


class EmailRecoverPassView(TemplateView):
    template_name = "main/pages/auth/recoverPass/emailRecover.html"

    def get(self, request, *args, **kwargs):
        # if not settings.ITS_APP:
        #     return redirect('app-download-page')
        context = self.get_context_data(**kwargs)
        context['title'] = "Password recovery"
        return redirect('main_page')
        if not request.user.is_anonymous:
            return redirect('profile-page')
        return self.render_to_response(context)


class PassRecoveryPost(View):
    def render_step(self, step):
        uval = self.request.POST.get('value') or ''
        return HttpResponse(dumps({
            'resp': "NS",
            'step': step,
            'uval': uval
        }))

    def render_error(self, msg, step, type=0):
        uval = self.request.POST.get('value') or ''
        return HttpResponse(dumps({
            'resp': "ERR",
            'step': step,
            'msg': msg,
            'uval': uval,
            'type': type
        }))

    def render_redirect(self, rev, get=''):
        return HttpResponse(dumps({
            'resp': "redirect",
            'rev': f"{resolve_url(rev)}{get}"
        }))

    def post(self, request, *args, **kwargs):
        type = request.POST.get('type')
        value = request.POST.get('value')
        code = request.POST.get('code')
        password = request.POST.get('password')
        prevstep = request.POST.get('prevstep')
        newcode = request.POST.get('newcode')
        user_model = get_user_model()
        print(request.POST)
        if request.user.is_anonymous:
            if type == "phone":
                if len(value) > 5:
                    user = user_model.objects.get_user_by_phone(value)
                    if user:
                        if newcode == 'true':
                            if check_seconds(user):
                                delete_code(user)
                                send_code(user, 'phone')
                                return self.render_error('New code has been sent to your phone.', 2, 1)
                        if len(code) > 0:
                            if check_recovery_sended(user):
                                if check_code(user, code):
                                    if len(password) > 6:
                                        user.set_password(password)
                                        user.save()
                                        delete_code(user)
                                        return self.render_redirect('login-form-page')
                                    else:
                                        if prevstep == 3:
                                            return self.render_error('Password cannot be smaller of 6 symbols.', 3)
                                        else:
                                            return self.render_error('', 3)
                                else:
                                    if prevstep == '2':
                                        return self.render_error('You entered wrong code', 2)
                                    else:
                                        return self.render_error('', 2)
                            else:
                                return self.render_error('Code has not sent.', 1)
                        else:
                            if check_recovery_sended(user):
                                if prevstep == '2':
                                    return self.render_error('You entered wrong code', 2)
                                else:
                                    return self.render_error('', 2)
                            else:
                                send_code(user, 'phone')
                                return self.render_step(2)
                    else:
                        return self.render_error("Phone is not registered.", 1)
                else:
                    return self.render_error("Phone number too short.", 1)
            elif type == 'email':
                if len(value) > 5:
                    user = user_model.objects.get_user_by_email(value)
                    if user:
                        if newcode == 'true':
                            if check_seconds(user):
                                delete_code(user)
                                send_code(user, 'email')
                                return self.render_error('New code has been sent to your email.', 2, 1)
                        if len(code) > 0:
                            if check_recovery_sended(user):
                                if check_code(user, code):
                                    if len(password) > 6:
                                        user.set_password(password)
                                        user.save()
                                        delete_code(user)
                                        return self.render_redirect('login-form-page', '?tab=2')
                                    else:
                                        if prevstep == 3:
                                            return self.render_error('Password cannot be smaller of 6 symbols.', 3)
                                        else:
                                            return self.render_error('', 3)
                                else:

                                    if prevstep == '2':
                                        return self.render_error('You entered wrong code', 2)
                                    else:
                                        return self.render_error('', 2)
                            else:
                                return self.render_error('Code has not sent.', 1)
                        else:
                            if check_recovery_sended(user):
                                if prevstep == '2':
                                    return self.render_error('You entered wrong code', 2)
                                else:
                                    return self.render_error('', 2)
                            else:
                                if not check_recovery_sended(user):
                                    send_code(user, 'email')
                                    return self.render_step(2)
                    else:
                        return self.render_error("Email is not registered.", 1)
                else:
                    return self.render_error("Email number too short.", 1)
        else:
            return self.render_redirect('profile-page')


class CodeVerificationView(TemplateView):
    template_name = "main/pages/auth/register/CodeVerification.html"

    def get(self, request, *args, **kwargs):
        # if not settings.ITS_APP:
        #     return redirect('app-download-page')
        context = self.get_context_data(**kwargs)
        context['title'] = 'Code verification'
        return redirect('main_page')
        if request.user.is_anonymous:
            return redirect('register-page')
        elif request.user.is_activated:
            return redirect('profile-page')
        # if not request.META.get('HTTP_REFERER'):
        #     request.session['errors'] = None
        # user_code = CodeActivation.objects.get(user=request.user)
        # user_code = request.user.user_code.all()[0]
        if request.user.phone:
            context['useract'] = request.user.phone
            context['usremail'] = False
        elif request.user.email:
            context['usremail'] = True
            context['useract'] = request.user.email
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('register-page')
        elif request.user.is_activated:
            return redirect('profile-page')
        context = self.get_context_data(**kwargs)
        code = request.POST.get('code')
        user_code = request.user.user_code.all()[0]
        if user_code.code == code:
            user_code.delete()
            request.user.is_activated = True
            request.user.save()
            return redirect('profile-creation')
        context['errors'] = ["You entered wrong code"]
        context['title'] = 'Code verification'
        return self.render_to_response(context)


class ProfileCreationView(TemplateView):
    template_name = 'main/pages/auth/register/ProfileCreation.html'

    def get(self, request, *args, **kwargs):
        # if not settings.ITS_APP:
        #     return redirect('app-download-page')
        return redirect('main_page')
        if request.user.is_anonymous:
            return redirect('register-page')
        elif not request.user.is_activated:
            return redirect('register-code-verificarion')
        if request.user.user_profile.all():
            return redirect('profile-page')
        context = self.get_context_data(**kwargs)
        list_of_genres_ids = [8, 10, 5, 20, 4, 33, 1, 19]
        list_of_sport_kinds_ids = [1, 2, 6, 4, 5]
        list_of_genres = []
        list_of_sport_kinds = []
        for id in list_of_genres_ids:
            try:
                list_of_genres.append(Genre.objects.get(id=id))
            except Genre.DoesNotExist:
                pass
        for id in list_of_sport_kinds_ids:
            try:
                list_of_sport_kinds.append(SportKind.objects.get(id=id))
            except SportKind.DoesNotExist:
                pass
        context['genres'] = list_of_genres
        context['sport_kinds'] = list_of_sport_kinds
        context['title'] = 'Profile creation'

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('register-page')
        elif not request.user.is_activated:
            return redirect('register-code-verificarion')
        if request.user.user_profile.all():
            return redirect('profile-page')
        context = self.get_context_data(**kwargs)
        name = request.POST.get('name')
        genres = request.POST.get('genres').split(',')
        for x in range(len(genres)):
            genres[x] = int(genres[x])
        sport = request.POST.get('sport').split(',')
        for x in range(len(sport)):
            sport[x] = int(sport[x])
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        user_profile = UserProfile(
            user=request.user,
            name=name,
            # genres = genres,
            # kinds = sport,
            gender=gender,
            age=age
        )
        user_profile.save()
        user_profile.genres.set(Genre.objects.filter(id__in=genres))
        user_profile.kinds.set(SportKind.objects.filter(id__in=sport))
        user_profile.save()
        return redirect('mode-change-page')


class LogoutUserView(View):
    def get(self, request, *args, **kwargs):
        # if not settings.ITS_APP:
        #     return redirect('app-download-page')
        if request.user.is_anonymous:
            return redirect('main_page')
        logout(request)
        return redirect('main_page')


class LoginView(TemplateView):
    template_name = "main/pages/auth/login/login.html"

    def get(self, request, *args, **kwargs):
        # if not settings.ITS_APP:
        #     return redirect('app-download-page')
        context = self.get_context_data(**kwargs)
        context.update({
            "title": "Login page"
        })
        return redirect('main_page')
        if request.user.is_anonymous:
            return self.render_to_response(context)
        elif not request.user.is_activated:
            return redirect('register-code-verificarion')
        return redirect('profile-page')


class LoginFormView(TemplateView):
    template_name = "main/pages/auth/login/loginForm.html"

    def get(self, request, *args, **kwargs):
        # if not settings.ITS_APP:
        #     return redirect('app-download-page')
        context = self.get_context_data(**kwargs)
        context['title'] = 'Login page'
        context['error_type'] = 0
        return redirect('main_page')
        if request.user.is_anonymous:
            return self.render_to_response(context)
        elif request.user.is_activated:
            return redirect('profile-page')
        return redirect('register-code-verificarion')

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        type_req = int(request.POST.get('type')) or 1
        username = request.POST.get('username') or ''
        password = request.POST.get('password') or ''
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if not user.is_activated:
                return redirect('register-code-verificarion')
            if not user.user_profile.all():
                return redirect('profile-creation')
            if user.user_profile.first().dark_mode:
                request.session['dark'] = True
            else:
                request.session['dark'] = False
            return redirect('profile-page')
        else:
            if type_req == 1:
                context['error_type'] = 1
                context['errors_phone_pass'] = ['Phone or password is not correct.']
            elif type_req == 2:
                context['error_type'] = 2
                context['errors_email_pass'] = ['Email or password is not correct.']
            context['title'] = 'Login page'
        return self.render_to_response(context)


# watchlist
class MovieAddToWatchlist(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            model = Movie.objects.get(id=pk)
        except Movie.DoesNotExist:
            raise Http404("Movie not found")
        if not request.user.is_anonymous:
            add_model_to_watchlist(request.user, model)
        else:
            return HttpResponse(dumps({
                'resp': "redirect",
                'rev': resolve_url('register-page')
            }))

        return HttpResponse(dumps({
            'resp': "OK"
        }))


class SerieAddToWatchlist(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            model = SerieEpisode.objects.get(id=pk)
        except SerieEpisode.DoesNotExist:
            raise Http404("Serie not found")
        if not request.user.is_anonymous:
            add_model_to_watchlist(request.user, model)
        else:
            return HttpResponse(dumps({
                'resp': "redirect",
                'rev': resolve_url('register-page')
            }))

        return HttpResponse(dumps({
            'resp': "OK"
        }))


class ShowAddToWatchlist(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            model = ShowEpisode.objects.get(id=pk)
        except ShowEpisode.DoesNotExist:
            raise Http404("Show not found")
        if not request.user.is_anonymous:
            add_model_to_watchlist(request.user, model)
        else:
            return HttpResponse(dumps({
                'resp': "redirect",
                'rev': resolve_url('register-page')
            }))

        return HttpResponse(dumps({
            'resp': "OK"
        }))


class ChannelAddToWatchlist(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            model = Channel.objects.get(id=pk)
        except Channel.DoesNotExist:
            raise Http404("Channel not found")
        if not request.user.is_anonymous:
            add_model_to_watchlist(request.user, model)
        else:
            return HttpResponse(dumps({
                'resp': "redirect",
                'rev': resolve_url('register-page')
            }))

        return HttpResponse(dumps({
            'resp': "OK"
        }))


class SendFeedbackView(TemplateView):
    template_name = 'main/pages/auth/sendFeedback.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.request.user.is_anonymous:
            return redirect('register-page')

        context['title'] = 'Feedback'
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.request.user.is_anonymous:
            return redirect('register-page')
        message = request.POST.get('feedback') or False
        if message and save_feedback_from_user(request.user, message):
            context['messages'] = [{"type": "good", "msg": "Your message has been sended."}]
        else:
            context['messages'] = [{"type": "bad", "msg": "Your message has not been sended."}]
        return self.render_to_response(context)


class RemoveFromWatchList(View):
    def post(self, request, *args, **kwargs):
        pk = int(request.POST.get('id'))
        type = int(request.POST.get('type'))
        if type == 1:
            try:
                model = Movie.objects.get(id=pk)
            except Movie.DoesNotExist:
                raise Http404('element not found')
        elif type == 2:
            try:
                model = SerieEpisode.objects.get(id=pk)
            except SerieEpisode.DoesNotExist:
                raise Http404('element not found')
        elif type == 3:
            try:
                model = ShowEpisode.objects.get(id=pk)
            except ShowEpisode.DoesNotExist:
                raise Http404('element not found')
        elif type == 4:
            try:
                model = Channel.objects.get(id=pk)
            except Channel.DoesNotExist:
                raise Http404('element not found')
        else:
            raise Http404('element not found')
        if not request.user.is_anonymous:
            add_model_to_watchlist(request.user, model)
        else:
            return HttpResponse(dumps({
                'resp': "redirect",
                'rev': resolve_url('register-page')
            }))

        return HttpResponse(dumps({
            'resp': "OK"
        }))


class RemoveFromHistoryList(View):
    def post(self, request, *args, **kwargs):
        pk = int(request.POST.get('id'))
        type = int(request.POST.get('type'))
        if type == 1:
            try:
                model = Movie.objects.get(id=pk)
            except Movie.DoesNotExist:
                raise Http404('element not found')
        elif type == 2:
            try:
                model = SerieEpisode.objects.get(id=pk)
            except SerieEpisode.DoesNotExist:
                raise Http404('element not found')
        elif type == 3:
            try:
                model = ShowEpisode.objects.get(id=pk)
            except ShowEpisode.DoesNotExist:
                raise Http404('element not found')
        else:
            raise Http404('element not found')
        if not request.user.is_anonymous:
            remove_from_history_model(request.user, model)
        else:
            return HttpResponse(dumps({
                'resp': "redirect",
                'rev': resolve_url('register-page')
            }))

        return HttpResponse(dumps({
            'resp': "OK"
        }))


class TermsOfUseView(TemplateView):
    template_name = 'main/pages/auth/termsOfUse.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['title'] = 'Terms of use'
        return self.render_to_response(context)


class PrivacyPolicyView(TemplateView):
    template_name = 'main/pages/auth/privacyPolicy.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['title'] = 'Privacy policy'
        return self.render_to_response(context)


class RemoveAccountFromVerification(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('main_page')
        if request.user.is_activated:
            return redirect('profile-page')

        request.user.delete()
        logout(request)
        return redirect('register-form-page')


class SettingsView(TemplateView):
    template_name = 'main/pages/auth/settings.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['title'] = 'Settings'
        return self.render_to_response(context)


class SubcriptionView(TemplateView):
    template_name = 'main/pages/auth/subscription.html'

    def get(self, request, *args, **kwargs):
        if not settings.ITS_APP:
            return redirect('app-download-page')
        if request.user.is_anonymous:
            return redirect('register-page')
        context = self.get_context_data(**kwargs)
        context['title'] = 'Subcriptions'
        context['sub'] = get_subscriptions_for_user(request.user)
        context['allsubs'] = Subscription.objects.all()

        return self.render_to_response(context)


class FirstTimeScreenView(TemplateView):
    template_name = 'main/pages/FirstTimeScreen.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['title'] = 'First start'
        return self.render_to_response(context)


class ModeChangeView(TemplateView):
    template_name = 'main/pages/changeMode.html'

    def get(self, request, *args, **kwargs):
        # if request.user.is_anonymous:
        #     return redirect('login-page')
        context = self.get_context_data(**kwargs)
        context['title'] = 'Mode change'
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        dark = request.POST.get('dark')
        if request.user.is_anonymous:
            if dark:
                request.session['dark'] = True
            else:
                request.session['dark'] = False
            return redirect('main_page')
        user_profile = request.user.user_profile.first()
        if dark:
            user_profile.dark_mode = True
        else:
            user_profile.dark_mode = False
        request.session['dark'] = user_profile.dark_mode
        user_profile.save()
        return redirect('profile-page')


class ModeChangePostView(View):
    def post(self, request, *args, **kwargs):
        dark = request.session.get('dark') or False
        if request.user.is_anonymous or not request.user.user_profile.first():
            if dark:
                request.session['dark'] = False
            else:
                request.session['dark'] = True
            return HttpResponse(dumps({
                'resp': "redirect",
                'rev': resolve_url('main_page')
            }))
        user_profile = request.user.user_profile.first()
        if dark:
            user_profile.dark_mode = False
        else:
            user_profile.dark_mode = True
        request.session['dark'] = user_profile.dark_mode
        user_profile.save()
        return HttpResponse(dumps({
            'resp': "redirect",
            'rev': resolve_url('main_page')
        }))


class SendComment(View):
    def post(self, request, *args, **kwargs):
        pk = int(request.POST.get('id'))
        type = int(request.POST.get('type'))
        query = request.POST.get('q')
        if type == 1:
            try:
                model = Movie.objects.get(id=pk)
            except Movie.DoesNotExist:
                raise Http404('element not found')
        elif type == 2:
            try:
                model = SerieEpisode.objects.get(id=pk)
            except SerieEpisode.DoesNotExist:
                raise Http404('element not found')
        elif type == 3:
            try:
                model = ShowEpisode.objects.get(id=pk)
            except ShowEpisode.DoesNotExist:
                raise Http404('element not found')
        elif type == 4:
            try:
                model = Sport.objects.get(id=pk)
            except Sport.DoesNotExist:
                raise Http404('element not found')
        else:
            raise Http404('element not found')
        if not request.user.is_anonymous:
            if not save_comment_for_model(request.user, model, query):
                return HttpResponse(dumps({
                    'resp': "ERR",
                    'msg': "Too fast sending comments."
                }))
            else:
                return HttpResponse(dumps({
                    'resp': "OK"
                }))
        else:
            return HttpResponse(dumps({
                'resp': "redirect",
                'rev': resolve_url('register-page')
            }))


class LikeComment(View):
    def post(self, request, *args, **kwargs):
        pk = int(request.POST.get('id'))
        if not request.user.is_anonymous:
            if not set_like_for_comment(request.user, pk):
                return HttpResponse(dumps({
                    'resp': "ERR",
                    'msg': 'can\'t set like'
                }))
            else:
                return HttpResponse(dumps({
                    'resp': "OK"
                }))
        else:
            return HttpResponse(dumps({
                'resp': "redirect",
                'rev': resolve_url('register-page')
            }))


class SetRating(View):
    def post(self, request, *args, **kwargs):
        model_id = int(request.POST.get('model_id'))
        ct_id = int(request.POST.get('ct_id'))
        grade = int(request.POST.get('grade'))
        if not request.user.is_anonymous:
            if not set_rating_for_model(model_id, ct_id, grade, request.user):
                return HttpResponse(dumps({
                    'resp': "ERR",
                    'msg': 'can\'t set like'
                }))
            else:
                return HttpResponse(dumps({
                    'resp': "OK"
                }))
        else:
            return HttpResponse(dumps({
                'resp': "redirect",
                'rev': resolve_url('register-page')
            }))


class GetNewRating(View):
    def post(self, request, *args, **kwargs):
        model_id = int(request.POST.get('model_id'))
        ct_id = int(request.POST.get('ct_id'))
        rating = get_rating_for_ct_model(model_id, ct_id)
        if not rating:
            return HttpResponse(dumps({
                'resp': "ERR",
                'msg': 'can\'t set like'
            }))
        else:
            return HttpResponse(dumps({
                'resp': "OK",
                'data': rating
            }))


class MinusAdf(View):
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            if not user.is_anonymous and user.user_profile.all():
                profile = user.user_profile.first()
                print(profile)
                current_time = profile.ad_free_time
                if current_time <= 0:
                    profile.ad_free_time = 0
                    profile.save()
                    return HttpResponse("not_ok")
                profile.ad_free_time = current_time - 10
                profile.save()
                return HttpResponse("ok")
        except Exception as e:
            return HttpResponse("not_ok")


class createShareUrl(View):
    def post(self, request, *args, **kwargs):
        url = request.POST.get('url')
        user = request.user
        if not user.is_anonymous and user.user_profile.all():
            if create_share_url(user, url):
                return HttpResponse("added")
            else:
                return HttpResponse("false")


class addDownload(View):
    def post(self, request, *args, **kwargs):
        url = request.POST.get('ref_url')
        if add_download_to_url(url):
            return HttpResponse("added")
        else:
            return HttpResponse("false")


class changeLocaleView(TemplateView):
    template_name = 'main/pages/settings/locale.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['title'] = 'Language'
        return self.render_to_response(context)


class downloadAppView(TemplateView):
    template_name = 'main/pages/appInstall.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        msg_id = request.GET.get('msg')
        if msg_id == '1':
            context['Message'] = gettext_noop(
                'You are now on preview. To continue watching for free , please install Zola TV official app.')
        context['title'] = 'Download app'
        url = self.request.build_absolute_uri()
        click_ref_link(url)
        return self.render_to_response(context)


class workInProgressView(TemplateView):
    template_name = 'main/pages/newfeatures.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['title'] = 'Work in progress'
        return self.render_to_response(context)


class buy1View(TemplateView):
    template_name = 'main/pages/buysub1.html'

    def get(self, request, *args, **kwargs):
        if not settings.ITS_APP:
            return redirect('app-download-page')
        context = self.get_context_data(**kwargs)
        context['title'] = 'Buy 1 month sub'
        return self.render_to_response(context)


class buy2View(TemplateView):
    template_name = 'main/pages/buysub2.html'

    def get(self, request, *args, **kwargs):
        if not settings.ITS_APP:
            return redirect('app-download-page')
        context = self.get_context_data(**kwargs)
        context['title'] = 'Buy 3 month sub'
        return self.render_to_response(context)


class getBonusView(TemplateView):
    template_name = 'main/pages/getBonus.html'

    def get(self, request, *args, **kwargs):
        if not settings.ITS_APP:
            return redirect('app-download-page')
        if request.user.is_anonymous:
            return redirect('register-page')
        context = self.get_context_data(**kwargs)
        context['allsubs'] = Subscription.objects.all()
        context['title'] = 'Get bonus'
        return self.render_to_response(context)


class GetPopup(TemplateView):
    def get_response(self, popups):
        result = []
        for popup in popups:
            if popup.active:
                result.append({"id": popup.id,
                               "name": popup.name,
                               "html": render_to_string(f"main/components/popups/{popup.template}.html"),
                               "show_times": popup.show_times,
                               "load_time": popup.load_time})
        return dumps(result)

    def get_popups_for_group(self, **queryset):
        user_groups = UserGroup.objects.filter(**queryset)
        popups = []
        for group in user_groups:
            for popup in group.popup.all():
                popups.append(popup)
        return popups

    def get_popups_by_time(self, u_time):
        user_groups = UserGroup.objects.filter(type='time_st')
        popups = []
        for group in user_groups:
            if int(now().timestamp()) - int(u_time.timestamp()) >= int(group.value):
                for popup in group.popup.all():
                    popups.append(popup)
        return popups

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        uid = request.POST.get('uid')
        try:
            user_info = FirstAnalytics.objects.get(u_id=uid)
            POPUPS = []
            POPUPS += self.get_popups_for_group(type='users', users__u_id__contains=uid)
            if len(user_info.a_id) > 0:
                POPUPS += self.get_popups_for_group(type='adid', value=user_info.a_id)
            POPUPS += self.get_popups_by_time(user_info.datetime)
            if request.user.is_anonymous:
                POPUPS += self.get_popups_for_group(type='nlog')
            return HttpResponse(self.get_response(POPUPS))
        except FirstAnalytics.DoesNotExist:
            return HttpResponse('Error')


class SendRating(View):
    def post(self, request, *args, **kwargs):
        uid = request.POST.get('uid')
        rating = int(request.POST.get('rating'))
        if rating > 5:
            rating = 5
        message = request.POST.get('message')
        print(uid)
        try:
            user = FirstAnalytics.objects.get(u_id=uid)
            try:
                act_rating = AppRating.objects.get(user=user)
                act_rating.rating = rating
                act_rating.comment = message
                act_rating.save()
                return HttpResponse('OK')
            except AppRating.DoesNotExist:
                pass
            new_rating = AppRating(
                user=user,
                rating=rating,
                comment=message
            )
            new_rating.save()
            return HttpResponse('OK')
        except FirstAnalytics.DoesNotExist:
            return HttpResponse('USER-ERROR')


class SubtitleLiveSearch(View):
    def post(self, request):
        return_count = 25
        try:
            search_query = request.POST.get('q')
            result_dict = dumps(SubtitleLiveSearchSerializer(
                Subtitle.objects.filter(file_name__icontains=search_query)[:return_count], many=True).data)
            return HttpResponse(dumps(result_dict, ensure_ascii=False), content_type="application/json; charset=utf-8")
        except KeyError:
            return HttpResponseNotFound()
