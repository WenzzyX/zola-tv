from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin
from django.contrib.admin import AdminSite
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin, UserAdmin, User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django import forms
from main.models import (
    Genre, Country, Language, SerieSeason, Subtitle,
    SportKind,
    ChannelProvider,
    Movie, MovieAltLang, Serie, SerieEpisode, Sport, Channel, Show, ShowSeason, ShowEpisode,
    Movielist, Serielist, Sportlist, Showlist, Channellist,
    Component, Page,
    Adbanner, AdVideo, AdVideoBanner, SerieEpAltLang, AdVideoMidroll, Setting, Popup
)

from users.models import Comment
from django.contrib.contenttypes.admin import GenericTabularInline


class CommentsInline(GenericTabularInline):
    model = Comment
    extra = 0
    fieldsets = (
        (None, {'fields': ('user', 'text', 'date')}),
    )
    readonly_fields = ('user', 'text', 'date')


class MovieAdmin(admin.ModelAdmin):
    def get_rating(self, obj):
        return obj.get_search_rating()

    get_rating.short_description = _("Пользовательский рейтинг")

    def copy_id(self, obj):
        return mark_safe(
            f'<div class="adm-copy">\
                <div class="adm-copy-success">Copied!</div>\
                <input class="adm-copy-input" type="text" value="{obj.id}" onclick="copyFromInput(this);" readonly>\
            </div>'
        )

    copy_id.short_description = _("ID for copy")

    def copy_imdb_id(self, obj):
        return mark_safe(
            f'<div class="adm-copy">\
                <div class="adm-copy-success">Copied!</div>\
                <input class="adm-copy-input" type="text" value="{obj.imdb_id}" onclick="copyFromInput(this);" readonly>\
            </div>'
        )

    copy_imdb_id.short_description = _("IMDB-ID for copy")

    def show_img(self, obj):
        return mark_safe(
            f'<img class="adm-object-poster" src="{obj.get_poster()}" alt="object_image">'
        )

    show_img.short_description = _("Poster")
    fieldsets = (
        (None, {'fields': ('name', 'year', 'genre', 'description')}),
        ('Video', {'fields': ('video_url',)}),
        ('Poster', {'fields': ('poster_url', 'big_poster_url')}),
        ('Info', {'fields': ('imdb_id', 'imdb_rating', 'duration', 'get_rating')}),
        ('Locale', {'fields': ('country', 'language')}),
        ('Subtitle', {'fields': ('subtitle_urls',)}),
        ('Settings', {'fields': ('imdb_link', 'date_pub', 'is_active')}),
        ('Analytics', {'fields': ('watch_counter',)}),
    )
    inlines = [CommentsInline]
    list_display = ('show_img', 'name', 'year', 'copy_id', 'imdb_id', 'copy_imdb_id', 'is_active')
    list_filter = ('year', 'language', 'genre', 'country')
    search_fields = ('name', 'imdb_id')
    ordering = ('name', 'year', 'imdb_id')
    save_on_top = True
    readonly_fields = ('get_rating', 'date_pub')
    list_display_links = ('name', 'show_img')


admin.site.register(Movie, MovieAdmin)


class MovieAltLangAdminForm(forms.ModelForm):
    class Meta:
        model = MovieAltLang
        fields = '__all__'
        widgets = {
            'movie': admin.widgets.AdminTextInputWidget
        }


class MovieAltLangAdmin(admin.ModelAdmin):
    form = MovieAltLangAdminForm

    fieldsets = (
        (None, {'fields': ('movie', 'language', 'video_url')}),
    )
    list_display = ('id', 'movie', 'movie_id', 'language')
    search_fields = ('movie__name', "movie__id")
    ordering = ('-id', 'movie')
    save_on_top = True


admin.site.register(MovieAltLang, MovieAltLangAdmin)


class SerieEpAltLangAdminForm(forms.ModelForm):
    class Meta:
        model = SerieEpAltLang
        fields = '__all__'
        widgets = {
            'episode': admin.widgets.AdminTextInputWidget
        }


class SerieEpAltLangAdmin(admin.ModelAdmin):
    form = SerieEpAltLangAdminForm

    fieldsets = (
        (None, {'fields': ('episode', 'language', 'video_url')}),
    )
    list_display = ('id', 'episode', 'episode_id', 'language')
    search_fields = ('episode__season__serie__name', "episode__id")
    list_display_links = ('episode',)
    ordering = ('-id', 'episode')
    save_on_top = True


admin.site.register(SerieEpAltLang, SerieEpAltLangAdmin)


class SerieAdmin(admin.ModelAdmin):
    def get_rating(self, obj):
        return obj.get_search_rating()

    get_rating.short_description = _("Пользовательский рейтинг")

    def copy_imdb_id(self, obj):
        return mark_safe(
            f'<div class="adm-copy">\
                <div class="adm-copy-success">Copied!</div>\
                <input class="adm-copy-input" type="text" value="{obj.imdb_id}" onclick="copyFromInput(this);" readonly>\
            </div>'
        )

    copy_imdb_id.short_description = _("IMDB-ID for copy")

    def show_img(self, obj):
        return mark_safe(
            f'<img class="adm-object-poster" src="{obj.get_poster()}" alt="object_image">'
        )

    show_img.short_description = _("Poster")
    fieldsets = (
        (None, {'fields': ('name', 'year', 'genre', 'description')}),
        ('Poster', {'fields': ('poster_url', 'big_poster_url')}),
        ('Info', {'fields': ('imdb_id', 'imdb_rating', 'get_rating')}),
        ('Locale', {'fields': ('country', 'language')}),
        ('Settings', {'fields': ('imdb_link', 'date_pub', 'is_active')}),
        ('Analytics', {'fields': ('watch_counter',)}),
    )
    list_display = ('show_img', 'name', 'year', 'imdb_id', 'copy_imdb_id', 'is_active')
    list_filter = ('year', 'language', 'genre', 'country')
    search_fields = ('name', 'imdb_id')
    ordering = ('name', 'year', 'imdb_id')
    save_on_top = True
    readonly_fields = ('get_rating', 'date_pub')
    list_display_links = ('name', 'show_img')


admin.site.register(Serie, SerieAdmin)


class SerieSeasonAdmin(admin.ModelAdmin):
    form = SerieEpAltLangAdminForm

    fieldsets = (
        (None, {'fields': ('serie', 'season_num')}),
    )
    list_display = ('serie', 'season_num')
    search_fields = ('serie__name',)
    ordering = ('serie',)
    save_on_top = True


admin.site.register(SerieSeason, SerieSeasonAdmin)


class SerieEpisodeAdmin(admin.ModelAdmin):
    def get_serie(self, obj):
        return obj.season.serie.name

    get_serie.short_description = "Сериал"

    def get_season_num(self, obj):
        return obj.season.season_num

    get_season_num.short_description = "Сезон"

    def copy_id(self, obj):
        return mark_safe(
            f'<div class="adm-copy">\
                <div class="adm-copy-success">Copied!</div>\
                <input class="adm-copy-input" type="text" value="{obj.id}" onclick="copyFromInput(this);" readonly>\
            </div>'
        )

    copy_id.short_description = _("ID for copy")

    def show_img(self, obj):
        return mark_safe(
            f'<img class="adm-object-preview" src="{obj.get_preview()}" alt="object_image">'
        )

    show_img.short_description = _("Preview")
    fieldsets = (
        (None, {'fields': ('episode_name', 'episode', 'season')}),
        ('Preview', {'fields': ('preview_url',)}),
        ('Video', {'fields': ('video_url',)}),
        ('Subtitle', {'fields': ('subtitle_urls',)}),
        ('Settings', {'fields': ('duration', 'date_pub', 'language')}),
        ('Analytics', {'fields': ('watch_counter',)}),
    )
    list_display = ('show_img', 'episode_name', 'episode', 'get_season_num', 'get_serie', 'episode_imdb_id', 'copy_id')
    list_filter = ('language',)
    inlines = [CommentsInline]
    search_fields = ('season__serie__name', 'id')
    ordering = ('season__season_num', 'episode', 'episode_name', 'episode_imdb_id')
    save_on_top = True
    readonly_fields = ('date_pub',)
    list_display_links = ('episode_name', 'show_img')


admin.site.register(SerieEpisode, SerieEpisodeAdmin)


# ---------------------

class ShowAdmin(admin.ModelAdmin):
    def get_rating(self, obj):
        return obj.get_search_rating()

    get_rating.short_description = _("Пользовательский рейтинг")

    def copy_imdb_id(self, obj):
        return mark_safe(
            f'<div class="adm-copy">\
                <div class="adm-copy-success">Copied!</div>\
                <input class="adm-copy-input" type="text" value="{obj.imdb_id}" onclick="copyFromInput(this);" readonly>\
            </div>'
        )

    copy_imdb_id.short_description = _("IMDB-ID for copy")

    def show_img(self, obj):
        return mark_safe(
            f'<img class="adm-object-poster" src="{obj.get_poster()}" alt="object_image">'
        )

    show_img.short_description = _("Poster")
    fieldsets = (
        (None, {'fields': ('name', 'year', 'genre', 'description')}),
        ('Poster', {'fields': ('poster_url', 'big_poster_url')}),
        ('Info', {'fields': ('imdb_id', 'imdb_rating', 'get_rating')}),
        ('Locale', {'fields': ('country', 'language')}),
        ('Settings', {'fields': ('imdb_link', 'date_pub', 'is_active')}),
        ('Analytics', {'fields': ('watch_counter',)}),
    )
    list_display = ('show_img', 'name', 'year', 'imdb_id', 'copy_imdb_id', 'is_active')
    list_filter = ('year', 'language', 'genre', 'country')
    search_fields = ('name', 'imdb_id')
    ordering = ('name', 'year', 'imdb_id')
    save_on_top = True
    readonly_fields = ('get_rating', 'date_pub')
    list_display_links = ('name', 'show_img')


admin.site.register(Show, ShowAdmin)


class ShowSeasonAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('show', 'season_num')}),
    )
    list_display = ('show', 'season_num')
    search_fields = ('show',)
    ordering = ('show',)
    save_on_top = True


admin.site.register(ShowSeason, ShowSeasonAdmin)


class ShowEpisodeAdmin(admin.ModelAdmin):
    def get_show(self, obj):
        return obj.season.show.name

    get_show.short_description = "Тв-шоу"

    def get_season_num(self, obj):
        return obj.season.season_num

    get_season_num.short_description = "Сезон"

    def show_img(self, obj):
        return mark_safe(
            f'<img class="adm-object-preview" src="{obj.get_preview()}" alt="object_image">'
        )

    show_img.short_description = _("Preview")
    fieldsets = (
        (None, {'fields': ('episode_name', 'episode', 'season')}),
        ('Preview', {'fields': ('preview_url',)}),
        ('Video', {'fields': ('video_url',)}),
        ('Subtitle', {'fields': ('subtitle_urls',)}),
        ('Settings', {'fields': ('duration', 'date_pub', 'language')}),
        ('Analytics', {'fields': ('watch_counter',)}),
    )
    list_display = ('show_img', 'episode_name', 'episode', 'get_season_num', 'get_show', 'episode_imdb_id')
    list_filter = ('season',)
    inlines = [CommentsInline]
    search_fields = ('season__show__name',)
    ordering = ('season__season_num', 'episode', 'episode_name', 'episode_imdb_id')
    save_on_top = True
    readonly_fields = ('date_pub',)
    list_display_links = ('episode_name', 'show_img')


admin.site.register(ShowEpisode, ShowEpisodeAdmin)


class SportAdmin(admin.ModelAdmin):
    def get_rating(self, obj):
        return obj.get_search_rating()

    get_rating.short_description = _("Пользовательский рейтинг")

    def copy_id(self, obj):
        return mark_safe(
            f'<div class="adm-copy">\
                <div class="adm-copy-success">Copied!</div>\
                <input class="adm-copy-input" type="text" value="{obj.id}" onclick="copyFromInput(this);" readonly>\
            </div>'
        )

    copy_id.short_description = _("ID")

    def show_img(self, obj):
        return mark_safe(
            f'<img class="adm-object-preview" src="{obj.get_poster()}" alt="object_image">'
        )

    show_img.short_description = _("Poster")
    fieldsets = (
        (None, {'fields': ('name', 'start', 'kind')}),
        ('Poster', {'fields': ('poster_url', 'big_poster_url')}),
        ('Video', {'fields': ('video_url',)}),
        ('Settings', {'fields': ('live_ch', 'get_rating', 'date_created', 'is_active')}),
        ('Locale', {'fields': ('language',)}),
        ('Analytics', {'fields': ('watch_counter',)}),
    )
    list_display = ('show_img', 'name', 'kind', 'start', 'copy_id', 'is_active')
    list_filter = ('kind',)
    inlines = [CommentsInline]
    search_fields = ('name',)
    ordering = ('name', 'kind', 'start')
    save_on_top = True
    list_display_links = ('name', 'show_img')
    readonly_fields = ('get_rating',)


admin.site.register(Sport, SportAdmin)


class SportKindAdmin(TranslationAdmin):
    def get_rating(self, obj):
        return obj.get_search_rating()

    get_rating.short_description = _("Пользовательский рейтинг")

    def show_img(self, obj):
        return mark_safe(
            f'<img class="adm-object-icon" src="{obj.get_icon()}" alt="object_image">'
        )

    show_img.short_description = _("icon")
    fieldsets = (
        (None, {'fields': ('name', 'icon')}),
    )
    list_display = ('name', 'show_img')
    search_fields = ('name',)
    ordering = ('name',)
    save_on_top = True
    # readonly_fields = ('date_pub',)


admin.site.register(SportKind, SportKindAdmin)


class ChannelAdmin(admin.ModelAdmin):
    def get_rating(self, obj):
        return obj.get_search_rating()

    get_rating.short_description = _("Пользовательский рейтинг")

    def show_img(self, obj):
        return mark_safe(
            f'<img class="adm-object-list" src="{obj.get_poster()}" alt="object_image">'
        )

    show_img.short_description = _("Poster")

    def copy_id(self, obj):
        return mark_safe(
            f'<div class="adm-copy">\
                <div class="adm-copy-success">Copied!</div>\
                <input class="adm-copy-input" type="text" value="{obj.id}" onclick="copyFromInput(this);" readonly>\
            </div>'
        )

    copy_id.short_description = _("ID")
    fieldsets = (
        (None, {'fields': ('name', 'provider', 'genre')}),
        ('Video', {'fields': ('get_url',)}),
        ('Poster', {'fields': ('poster_url', 'preview_url', 'big_poster_url')}),
        ('Settings', {'fields': ('get_rating', 'is_iptv', 'is_active')}),
        ('Locale', {'fields': ('country', 'language')}),
        ('Analytics', {'fields': ('watch_counter',)}),
    )
    list_display = ('show_img', 'name', 'provider', 'copy_id', 'is_iptv', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_iptv', 'country', 'language', 'genre')
    inlines = [CommentsInline]
    ordering = ('name', 'is_iptv')
    save_on_top = True
    list_display_links = ('name', 'show_img')
    readonly_fields = ('get_rating',)


admin.site.register(Channel, ChannelAdmin)


class ChannelProviderAdmin(admin.ModelAdmin):
    def show_img(self, obj):
        return mark_safe(
            f'<img class="adm-object-list" src="{obj.get_poster()}" alt="object_image">'
        )

    show_img.short_description = _("Poster")

    def copy_id(self, obj):
        return mark_safe(
            f'<div class="adm-copy">\
                <div class="adm-copy-success">Copied!</div>\
                <input class="adm-copy-input" type="text" value="{obj.id}" onclick="copyFromInput(this);" readonly>\
            </div>'
        )

    copy_id.short_description = _("ID")
    fieldsets = (
        (None, {'fields': ('name', 'genre')}),
        ('Poster', {'fields': ('poster_url', 'poster', 'poster_ch')}),
        ('Locale', {'fields': ('based', 'language')}),
    )
    list_display = ('show_img', 'name', 'copy_id')
    search_fields = ('name',)
    list_filter = ('language', 'genre', 'based')
    ordering = ('name',)
    save_on_top = True
    list_display_links = ('name', 'show_img')


admin.site.register(ChannelProvider, ChannelProviderAdmin)


class GenreAdmin(TranslationAdmin):
    def show_img(self, obj):
        return mark_safe(
            f'<img class="adm-object-icon" src="{obj.get_icon()}" alt="object_image">'
        )

    show_img.short_description = _("icon")
    fieldsets = (
        (None, {'fields': ('name', 'icon')}),
    )
    list_display = ('name', 'show_img')
    search_fields = ('name',)
    ordering = ('name',)
    save_on_top = True
    # readonly_fields = ('date_pub',)


admin.site.register(Genre, GenreAdmin)

class SubtitleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('file_name', 'file_extension', 'language')}),
    )
    list_display = ('file_name', 'file_extension', 'language')
    search_fields = ('file_name', 'language')
    ordering = ('file_name',)
    save_on_top = True
    # readonly_fields = ('date_pub',)


admin.site.register(Subtitle, SubtitleAdmin)


class CountryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'iso3', 'iso3_code')}),
    )
    list_display = ('name', 'iso3', 'iso3_code')
    search_fields = ('name',)
    ordering = ('name',)
    save_on_top = True
    # readonly_fields = ('date_pub',)


admin.site.register(Country, CountryAdmin)


class LanguageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'iso3', 'iso3_code')}),
    )
    list_display = ('name', 'iso3', 'iso3_code')
    search_fields = ('name',)
    ordering = ('name',)
    save_on_top = True
    # readonly_fields = ('date_pub',)


admin.site.register(Language, LanguageAdmin)


class MovieListAdmin(admin.ModelAdmin):
    def show_img(self, obj):
        return mark_safe(
            f'<img class="adm-object-list" src="{obj.get_poster()}" alt="object_image">'
        )

    show_img.short_description = _("Poster")

    def copy_id(self, obj):
        return mark_safe(
            f'<div class="adm-copy">\
                <div class="adm-copy-success">Copied!</div>\
                <input class="adm-copy-input" type="text" value="{obj.id}" onclick="copyFromInput(this);" readonly>\
            </div>'
        )

    copy_id.short_description = _("ID")
    fieldsets = (
        (None, {'fields': ('name', 'sort_method')}),
        ('Poster', {'fields': ('poster_url',)}),
        # ('Settings', {'fields': ('hide')}),

    )
    list_display = ('show_img', 'name', 'copy_id')
    search_fields = ('name',)
    ordering = ('name',)
    save_on_top = True
    list_display_links = ('name', 'show_img')
    # readonly_fields = ('date_pub',)


admin.site.register(Movielist, MovieListAdmin)


class SerieListAdmin(admin.ModelAdmin):
    def show_img(self, obj):
        return mark_safe(
            f'<img class="adm-object-list" src="{obj.get_poster()}" alt="object_image">'
        )

    show_img.short_description = _("Poster")

    def copy_id(self, obj):
        return mark_safe(
            f'<div class="adm-copy">\
                <div class="adm-copy-success">Copied!</div>\
                <input class="adm-copy-input" type="text" value="{obj.id}" onclick="copyFromInput(this);" readonly>\
            </div>'
        )

    copy_id.short_description = _("ID")
    fieldsets = (
        (None, {'fields': ('name', 'sort_method')}),
        ('Poster', {'fields': ('poster_url',)}),
        # ('Settings', {'fields': ('hide')}),

    )
    list_display = ('show_img', 'name', 'copy_id')
    search_fields = ('name',)
    ordering = ('name',)
    save_on_top = True
    list_display_links = ('name', 'show_img')
    # readonly_fields = ('date_pub',)


admin.site.register(Serielist, SerieListAdmin)


class SportListAdmin(admin.ModelAdmin):
    def show_img(self, obj):
        return mark_safe(
            f'<img class="adm-object-list" src="{obj.get_poster()}" alt="object_image">'
        )

    show_img.short_description = _("Poster")

    def copy_id(self, obj):
        return mark_safe(
            f'<div class="adm-copy">\
                <div class="adm-copy-success">Copied!</div>\
                <input class="adm-copy-input" type="text" value="{obj.id}" onclick="copyFromInput(this);" readonly>\
            </div>'
        )

    copy_id.short_description = _("ID")
    fieldsets = (
        (None, {'fields': ('name', 'sort_method')}),
        ('Poster', {'fields': ('poster_url',)}),
        # ('Settings', {'fields': ('hide')}),

    )
    list_display = ('show_img', 'name', 'copy_id')
    search_fields = ('name',)
    ordering = ('name',)
    save_on_top = True
    list_display_links = ('name', 'show_img')
    # readonly_fields = ('date_pub',)


admin.site.register(Sportlist, SportListAdmin)


class ShowListAdmin(admin.ModelAdmin):
    def show_img(self, obj):
        return mark_safe(
            f'<img class="adm-object-list" src="{obj.get_poster()}" alt="object_image">'
        )

    show_img.short_description = _("Poster")

    def copy_id(self, obj):
        return mark_safe(
            f'<div class="adm-copy">\
                <div class="adm-copy-success">Copied!</div>\
                <input class="adm-copy-input" type="text" value="{obj.id}" onclick="copyFromInput(this);" readonly>\
            </div>'
        )

    copy_id.short_description = _("ID")
    fieldsets = (
        (None, {'fields': ('name', 'sort_method')}),
        ('Poster', {'fields': ('poster_url',)}),
        # ('Settings', {'fields': ('hide')}),

    )
    list_display = ('show_img', 'name', 'copy_id')
    search_fields = ('name',)
    ordering = ('name',)
    save_on_top = True
    list_display_links = ('name', 'show_img')
    # readonly_fields = ('date_pub',)


admin.site.register(Showlist, ShowListAdmin)


class ChannelListAdmin(admin.ModelAdmin):
    def show_img(self, obj):
        return mark_safe(
            f'<img class="adm-object-list" src="{obj.get_poster()}" alt="object_image">'
        )

    show_img.short_description = _("Poster")

    def copy_id(self, obj):
        return mark_safe(
            f'<div class="adm-copy">\
                <div class="adm-copy-success">Copied!</div>\
                <input class="adm-copy-input" type="text" value="{obj.id}" onclick="copyFromInput(this);" readonly>\
            </div>'
        )

    copy_id.short_description = _("ID")
    fieldsets = (
        (None, {'fields': ('name', 'sort_method')}),
        ('Poster', {'fields': ('poster_url',)}),
        # ('Settings', {'fields': ('hide')}),

    )
    list_display = ('show_img', 'name', 'copy_id')
    search_fields = ('name',)
    ordering = ('name',)
    save_on_top = True
    list_display_links = ('name', 'show_img')
    # readonly_fields = ('date_pub',)


admin.site.register(Channellist, ChannelListAdmin)


class ComponentAdmin(TranslationAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'name_on_page')}),
        ('Settings', {'fields': ('handler', 'path')}),
        ('Sort', {'fields': ('sort_method',)}),
        # ('Settings', {'fields': ('hide')}),

    )
    list_display = ('name', 'name_on_page', 'handler')
    search_fields = ('name',)
    ordering = ('name',)
    save_on_top = True
    list_display_links = ('name',)
    # readonly_fields = ('date_pub',)


admin.site.register(Component, ComponentAdmin)
admin.site.register(Page)


class AdbannerAdmin(admin.ModelAdmin):
    def copy_id(self, obj):
        return mark_safe(
            f'<div class="adm-copy">\
                <div class="adm-copy-success">Copied!</div>\
                <input class="adm-copy-input" type="text" value="{obj.id}" onclick="copyFromInput(this);" readonly>\
            </div>'
        )

    copy_id.short_description = _("ID")
    fieldsets = (
        (None, {'fields': ('name', 'template', 'links',)}),
        ('Image', {'fields': ('banner_url',)}),
        # ('Settings', {'fields': ('hide')}),

    )
    list_display = ('name', 'copy_id')
    search_fields = ('name',)
    ordering = ('name',)
    save_on_top = True
    # readonly_fields = ('date_pub',)


admin.site.register(Adbanner, AdbannerAdmin)
admin.site.register(AdVideo)
admin.site.register(AdVideoBanner)
admin.site.register(AdVideoMidroll)


class SettingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('t_id', 'type', 'value',)}),
    )
    list_display = ('type', 'value')
    search_fields = ('type',)
    ordering = ('type',)
    save_on_top = True
    list_display_links = ('type',)


admin.site.register(Setting, SettingAdmin)


class PopupAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'group',)}),
        ("Settings", {'fields': ('show_times', 'load_time', 'active')}),
        ("View", {'fields': ('template',)}),
    )
    list_display = ('name', 'group', 'active')
    search_fields = ('name',)
    ordering = ('name', 'group')
    save_on_top = True
    list_display_links = ('name',)


admin.site.register(Popup, PopupAdmin)
