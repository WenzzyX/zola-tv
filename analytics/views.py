from django.views.generic import TemplateView, View
from django.shortcuts import redirect, reverse
from main.models import Movie, Serie, Channel, Show, Sport, Adbanner, AdVideoBanner, AdVideoMidroll
from users.models import UserProfile, CustomUser, Comment, UserFeedback, RefLink
from analytics.models import EventAnalytics, BannerAnalytics
from analytics.utils.watch_analytics import save_event, save_first
from analytics.utils.views_analytics import clear_all_views
from django.shortcuts import HttpResponse
from operator import itemgetter, attrgetter
from datetime import datetime
from django.utils.timezone import now
from django.db.models import Q



class AnalyticsPageView(TemplateView):
    template_name = 'admin/analytics/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('admin:login')

        context = self.get_context_data(**kwargs)
        Groups = ["Analytic"]
        if request.user.is_adm:
            flag = False
            if request.user.is_superuser:
                flag = True
                context['has_permissions'] = True
            else:
                for el in Groups:
                    if el in list(request.user.groups.all().values_list("name", flat=True)):
                        context['has_permissions'] = True
                        flag = True
                        break
            if not flag:
                return redirect('admin:login')
        else:
            return redirect('admin:login')
        context['top_10_movies'] = Movie.objects.all().order_by('-watch_counter')[:30]
        context['top_10_series'] = Serie.objects.all().order_by('-watch_counter')[:30]
        context['top_10_channels'] = Channel.objects.all().order_by('-watch_counter')[:30]
        context['top_10_shows'] = Show.objects.all().order_by('-watch_counter')[:30]
        context['top_10_sport'] = Sport.objects.all().order_by('-watch_counter')[:30]

        top_10_by_views = []
        for el in context['top_10_movies']:
            top_10_by_views.append(el)
        for el in context['top_10_series']:
            top_10_by_views.append(el)
        for el in context['top_10_channels']:
            top_10_by_views.append(el)
        for el in context['top_10_shows']:
            top_10_by_views.append(el)
        for el in context['top_10_sport']:
            top_10_by_views.append(el)
        context['top_10_by_views'] = sorted(top_10_by_views, key=attrgetter('watch_counter'), reverse=True)[:30]
        context['title_top'] = 'Analytics | ZolaTV'

        # d_lte, d_gte = request.GET.get('date_lte'), request.GET.get('date_gte')
        # if d_lte != None and d_gte != None:
        #     d_lte, d_gte = d_lte.replace("%3A", ":"), d_gte.replace("%3A", ":")
        #     context['d_lte'], context['d_gte']  = d_lte, d_gte
        #     d_lte, d_gte = datetime.strptime(d_lte, '%Y-%m-%dT%H:%M'), datetime.strptime(d_gte, '%Y-%m-%dT%H:%M')
        #     all_clicks_banners = BannerAnalytics.objects.filter(datetime__gte=d_lte, datetime__lte=d_gte)
        #     all_clicks_events = EventAnalytics.objects.filter(datetime__gte=d_lte, datetime__lte=d_gte)
        #

        d_lte, d_gte = request.GET.get('date_lte'), request.GET.get('date_gte')
        if d_lte != None and d_gte != None:
            d_lte, d_gte = d_lte.replace("%3A", ":"), d_gte.replace("%3A", ":")
            context['d_lte'] = d_lte
            context['d_gte'] = d_gte
            d_lte, d_gte = datetime.strptime(d_lte, '%Y-%m-%dT%H:%M'), datetime.strptime(d_gte, '%Y-%m-%dT%H:%M')
            banners_clicks = BannerAnalytics.objects.filter(datetime__gte=d_lte, datetime__lte=d_gte)
            events_clicks = EventAnalytics.objects.filter(datetime__gte=d_lte, datetime__lte=d_gte)
        else:
            banners_clicks = BannerAnalytics.objects.all()
            events_clicks = EventAnalytics.objects.all()
        banners_objids = banners_clicks.values_list('object_id', flat=True).distinct()
        banners_dict = {}
        for banner in banners_objids:
            if d_lte != None and d_gte != None:
                clicks = BannerAnalytics.objects.filter(object_id=banner, datetime__gte=d_lte, datetime__lte=d_gte)
            else:
                clicks = BannerAnalytics.objects.filter(object_id=banner)
            countries = clicks.values_list('country', flat=True).distinct()
            name = 'Can\'t find name'
            link = ''
            try:
                obj = Adbanner.objects.get(id=int(banner))
                name = obj.name
                link = f"/admin/main/adbanner/{banner}"
            except:
                try:
                    obj = AdVideoMidroll.objects.get(id=int(banner))
                    name = obj.name
                    link = f"/admin/main/advideomidroll/{banner}"
                except:
                    try:
                        obj = AdVideoBanner.objects.get(id=int(banner))
                        name = obj.name
                        link = f"/admin/main/advideobanner/{banner}"
                    except:
                        pass


            banners_dict[f"{banner}"] = {"content": [], "name": name, "link": link}
            for elem in countries:
                if d_lte != None and d_gte != None:
                    clicks = BannerAnalytics.objects.filter(object_id=banner, country=elem, datetime__gte=d_lte, datetime__lte=d_gte)
                else:
                    clicks = BannerAnalytics.objects.filter(object_id=banner, country=elem)
                count_clicks = clicks.values_list('type', flat=True)
                cl_b = count_clicks.filter(~Q(type='sh_vid_b')).count()
                s_vid_b = count_clicks.filter(type='sh_vid_b').count()
                if s_vid_b > 0:
                    banners_dict[f"{banner}"]['shows_on'] = True
                banners_dict[f"{banner}"]['content'].append({"country": elem, "clicks": cl_b, "shows": s_vid_b})
        context['default_date'] = now().strftime('%Y-%m-%dT%H:%M')
        context['banners'] = banners_dict
        events = events_clicks.values_list('type', flat=True).distinct()
        event_final = {}
        for event in events:
            event_final[f"{event}"] = {"content": [], "name": event, "link": "/admin/analytics/eventanalytics/"}
            if d_lte != None and d_gte != None:
                objs_event = EventAnalytics.objects.filter(type=event, datetime__gte=d_lte, datetime__lte=d_gte)
            else:
                objs_event = EventAnalytics.objects.filter(type=event)
            objs_event_countr = objs_event.values_list('country', flat=True).distinct()
            for countr in objs_event_countr:
                if d_lte != None and d_gte != None:
                    objs_event_clicks = EventAnalytics.objects.filter(type=event, country=countr, datetime__gte=d_lte, datetime__lte=d_gte).count()
                else:
                    objs_event_clicks = EventAnalytics.objects.filter(type=event, country=countr).count()
                event_final[f"{event}"]['content'].append({"country": countr, "clicks": objs_event_clicks})
        context['events'] = event_final

        context['main_stats'] = []
        context['main_stats'].append({"name": "Users", "value": CustomUser.objects.count()})
        context['main_stats'].append({"name": "Activated users", "value": CustomUser.objects.filter(is_activated=True).count()})
        context['main_stats'].append({"name": "User profiles", "value": UserProfile.objects.count()})
        context['main_stats'].append({"name": "Comments count", "value": Comment.objects.count()})
        context['main_stats'].append({"name": "Feedbacks count", "value": UserFeedback.objects.count()})
        context['main_stats'].append({"name": "Referal links count", "value": RefLink.objects.count()})
        context['main_stats'].append({"name": "Movies count", "value": Movie.objects.count()})
        context['main_stats'].append({"name": "Series count", "value": Serie.objects.count()})
        context['main_stats'].append({"name": "Shows count", "value": Show.objects.count()})
        context['main_stats'].append({"name": "Channels count", "value": Channel.objects.count()})
        context['main_stats'].append({"name": "Sports count", "value": Sport.objects.count()})


        return self.render_to_response(context)


class SaveEventView(View):
    def post(self, request, *args, **kwargs):
        return HttpResponse(save_event(request))

class SaveFirstView(View):
    def post(self, request, *args, **kwargs):
        return HttpResponse(save_first(request))

class ClearViews(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('admin:login')
        if request.user.is_superuser:
            pass
        else:
            Groups = ["Analytic"]
            flag = False
            for el in Groups:
                if el in list(request.user.groups.all().values_list("name", flat=True)):
                    flag = True
                    break
            if not flag:
                return redirect('admin:login')

        clear_all_views()
        return redirect('analytics-page')