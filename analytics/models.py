from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class BannerAnalytics(models.Model):
    type = models.CharField('Тип события', max_length=255)
    url = models.CharField('URL запроса', max_length=512)
    user_agent = models.CharField('User Agent', max_length=512)
    accept_language = models.CharField('Accept language', max_length=512)
    ip = models.CharField('ip', max_length=255)
    country = models.CharField('Страна', max_length=128)
    datetime = models.DateTimeField("Время события")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.content_object}'

    class Meta:
        verbose_name = "Аналитика баннера"
        verbose_name_plural = "Аналитика баннеров"


class EventAnalytics(models.Model):
    type = models.CharField('Тип события', max_length=255)
    url = models.CharField('URL запроса', max_length=512)
    user_agent = models.CharField('User Agent', max_length=512)
    accept_language = models.CharField('Accept language', max_length=512)
    ip = models.CharField('ip', max_length=255)
    country = models.CharField('Страна', max_length=128)
    datetime = models.DateTimeField("Время события")

    def __str__(self):
        return f'{self.ip}'

    class Meta:
        verbose_name = "Аналитика события"
        verbose_name_plural = "Аналитика событий"


class FirstAnalytics(models.Model):
    u_id = models.CharField("Уникальный id юзера", max_length=255, unique=True)
    a_id = models.CharField("Уникальный id рекламы", max_length=255, default='')
    url = models.CharField('URL запроса', max_length=512)
    user_agent = models.CharField('User Agent', max_length=512)
    accept_language = models.CharField('Accept language', max_length=512)
    ip = models.CharField('ip', max_length=255)
    country = models.CharField('Страна', max_length=128)
    datetime = models.DateTimeField("Время события")

    def __str__(self):
        return f'{self.u_id}'

    class Meta:
        verbose_name = "Аналитика первого посещения"
        verbose_name_plural = "Аналитика первых посещений"
