from modeltranslation.translator import register, TranslationOptions
from main.models import SportKind, Genre, Component


@register(SportKind)
class SportKindTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Component)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name_on_page',)