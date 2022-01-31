from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from main.models import (Genre, SportKind, Movie, SerieEpisode, ShowEpisode, Sport, Channel)
from users.userActivation import get_random_code
from django.core.mail import send_mail
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from sms import send_sms
from django.conf import settings
from django.utils.translation import gettext_noop


class CustomUserManager(BaseUserManager):
    def send_mail(self, to, message):
        emails = []
        emails.append(to)
        send_mail('ZolaTV | Registration', message, 'best.cinema.app@gmail.com', emails, fail_silently=True)

    def send_sms(self, to, message):
        phones = []
        phones.append(to)
        send_sms(
            body=message,
            originator=settings.TWILIO_PHONE_NUMBER,
            recipients=phones,
            fail_silently=True
        )

    def create_code_for_new_user(self, user):
        generated_code = get_random_code()
        code = CodeActivation(
            user=user,
            code=generated_code
        )
        if user.email:
            code.is_email = True
            print('EMAIL')
            self.send_mail(to=user.email, message=f"You're code for activate account on ZolaTV is: {generated_code}")
        elif user.phone:
            print('PHONE')
            self.send_sms(to=f'+{user.phone}',
                          message=f"You're code for activate account on ZolaTV is: {generated_code}")
        code.save()

    def create_user_out(self,
                        email='',
                        phone='',
                        password=None,
                        ip=''):
        if (not phone) and (not email) or (len(password) < 6):
            return False

        user = self.model(
            email=self.normalize_email(email),
            phone=self.normalize_phone(phone),
            ip=ip
        )
        user.set_password(password)
        # user.is_superuser = True
        user.save(using=self._db)
        self.create_code_for_new_user(user)
        return user

    def create_user(self,
                    email='',
                    phone='',
                    password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if (not phone) and (not email):
            raise ValueError('Users must have an phone number or email address')

        user = self.model(
            email=self.normalize_email(email),
            phone=self.normalize_phone(phone),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         email='',
                         phone='',
                         password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            phone=self.normalize_phone(phone),
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

    @classmethod
    def normalize_phone(cls, phone):
        replacements = {"+": "", " ": ""}
        return "".join([replacements.get(c, c) for c in phone])

    def get_user_by_phone(self, phone):
        try:
            return CustomUser.objects.get(phone=phone)
        except CustomUser.DoesNotExist:
            return False

    def get_user_by_email(self, email):
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return False


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email', max_length=255, blank=True, null=True, unique=True)
    phone = models.CharField(verbose_name='Phone', max_length=255, blank=True, null=True, unique=True)
    ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='Register IP')
    last_login_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='Last-login IP')
    is_activated = models.BooleanField(verbose_name="User activated", default=False)
    is_active = models.BooleanField(verbose_name="User active", default=True)
    is_adm = models.BooleanField(verbose_name="User staff", default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'phone'
    ]

    # def get_username(self):
    #     return self.name
    #     # super().get_username()
    def save(self, *args, **kwargs):
        if not self.email:
            self.email = None
        if not self.phone:
            self.phone = None
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.email or self.phone

    def has_module_perms(self, app_label):
        return self.is_adm

    def has_perm(self, perm, obj=None):
        from django.contrib.auth.backends import ModelBackend
        return ModelBackend.has_perm(self=ModelBackend(),user_obj=self, perm=perm, obj=obj)

    @property
    def is_staff(self):
        return self.is_adm

    class Meta:
        verbose_name = "Прользователь"
        verbose_name_plural = "Прользователи"


class CodeActivation(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="User", on_delete=models.CASCADE, related_name='user_code')
    is_email = models.BooleanField(verbose_name="User use email?", default=False)
    code = models.CharField(verbose_name="Code for activate", max_length=255)

    def __str__(self):
        return self.user.email or self.user.phone

    class Meta:
        verbose_name = "Код активации"
        verbose_name_plural = "Коды активации"


class CodeRecovery(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="User", on_delete=models.CASCADE,
                             related_name='user_code_recover')
    is_email = models.BooleanField(verbose_name="User use email?", default=False)
    time = models.DateTimeField(verbose_name="Time of sent", auto_now=True)
    code = models.CharField(verbose_name="Code for recovery", max_length=255)

    def __str__(self):
        return self.user.email or self.user.phone

    class Meta:
        verbose_name = "Код восстановления"
        verbose_name_plural = "Коды восстановления"


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('1', gettext_noop('male')),
        ('2', gettext_noop('female'))
    )
    AGE_CHOICES = (
        ('1', gettext_noop('Under 18')),
        ('2', '18-30'),
        ('3', '30-45'),
        ('4', '45-60'),
        ('5', '60+'),
    )
    user = models.ForeignKey(CustomUser, verbose_name="User", on_delete=models.CASCADE, related_name='user_profile')
    name = models.CharField(verbose_name='Name', max_length=255)
    genres = models.ManyToManyField(Genre, verbose_name="Genres")
    kinds = models.ManyToManyField(SportKind, verbose_name="Sport kinds")
    gender = models.CharField(verbose_name='Gender', max_length=20, choices=GENDER_CHOICES, default='1')
    age = models.CharField(verbose_name='Age', max_length=20, choices=AGE_CHOICES, default='1')
    avatar = models.ImageField("User avatar", upload_to='uploads/users/avatars', null=True, blank=True)
    avatar_url = models.CharField("User avatar url", max_length=255, null=True, blank=True)
    avatar_ch = models.BooleanField("User choice avatar or url", default=False)
    dark_mode = models.BooleanField("Dark_mode", default=False)
    ad_free_time = models.PositiveIntegerField("Ad free time", default=0)

    def __str__(self):
        return self.name

    def get_avatar(self):
        if (self.avatar_ch):
            return self.avatar_url
        else:
            if self.avatar:
                return f"/media/{self.avatar}"
            else:
                return ''

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"


class UserWatchHisory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='watchhistory')
    date = models.DateTimeField('Time', auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"UserHistory for {self.user}"

    class Meta:
        verbose_name = "История пользователя"
        verbose_name_plural = "Истории пользователей"


class UserWatchList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='watchlist')
    date = models.DateTimeField('Time', auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"UserWatchHistory for {self.user}"

    class Meta:
        verbose_name = "Watchlist пользователя"
        verbose_name_plural = "Watchlists пользователей"


class UserFeedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='feedback')
    text = models.TextField(verbose_name='Feedback Text', max_length=5000)
    date = models.DateTimeField(verbose_name='Date of get', auto_now_add=True)

    def __str__(self):
        return f"UserFeedback from {self.user}"

    class Meta:
        verbose_name = "Обратная связь пользователя"
        verbose_name_plural = "Обратная связь пользователей"


class Subscription(models.Model):
    name = models.CharField("Name", max_length=255)
    term = models.IntegerField("Term of sub (days)", default=30)
    discount_price = models.CharField("Discount price", max_length=100, default="4.99")
    price = models.CharField("Price", max_length=100, default='2.99')
    economy = models.CharField("Economy", max_length=100, default="10%", blank=True)
    show_economy = models.BooleanField(verbose_name="Show economy", default=False)

    def __str__(self):
        return self.name

    def get_term_in_months(self):
        return round(self.term / 30)

    def get_economy(self):
        if self.show_economy:
            return self.economy
        return ''

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class UserSubscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sub")
    subscription = models.ForeignKey(Subscription, null=True, on_delete=models.SET_NULL)
    date_begin = models.DateTimeField(verbose_name="Date of begin", default=timezone.now)

    def get_date_end(self):
        return self.date_begin + timedelta(days=self.subscription.term)

    def __str__(self):
        return f"Sub for {self.user}"

    class Meta:
        verbose_name = "Подписка пользователя"
        verbose_name_plural = "Подписки пользователей"


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="User", on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=1000, default='')
    date = models.DateTimeField(verbose_name="date added", auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.content_object}'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="like")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="like")

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = "Лайк комментария"
        verbose_name_plural = "Лайки комментариев"


class Rating(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="User", on_delete=models.CASCADE, related_name="ratings")
    grade = models.PositiveIntegerField(verbose_name="grade")
    date = models.DateTimeField(verbose_name="date added", auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = "Рейтинг пользователя"
        verbose_name_plural = "Рейтинги пользователей"


class RefLink(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="User", on_delete=models.CASCADE, related_name="reflinks")
    link = models.TextField("Link", blank=False)
    clicks = models.PositiveIntegerField("Clicks", default=0)
    downloads = models.PositiveIntegerField("Downloads", default=0)
    date = models.DateTimeField(verbose_name="date added", auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = "Реф-ссылка пользователя"
        verbose_name_plural = "Реф-ссылки пользователей"


class UserGroup(models.Model):
    T_CHOICES = (
        ('time_st', "Время использования после начала"),
        ('users', "Выбранные пользователи"),
        ('adid', "Рекламный id"),
        ('nlog', "Не залогиненые пользователи"),
    )
    TAR_CHOICES = (
        ('movie', "Кино"),
        ('sport', "Спорт"),
    )
    GENDER_CHOICES = (
        ('1', "Мужчина"),
        ('2', "Женщина")
    )
    name = models.CharField('Название группы', max_length=255)
    users = models.ManyToManyField("analytics.FirstAnalytics", verbose_name="Пользователи")
    type = models.CharField('Тип группы', choices=T_CHOICES, max_length=255)
    value = models.CharField('Параметр', max_length=255, default='', blank=True)
    age = models.PositiveIntegerField('Возраст (от)', default=0, blank=True)
    age_to = models.PositiveIntegerField('Возраст (до)', default=0, blank=True)
    gender = models.CharField('Пол', choices=GENDER_CHOICES, max_length=50, default='', blank=True)
    location = models.CharField('Локация', max_length=512, default='', blank=True)
    target = models.CharField('Цель', choices=TAR_CHOICES, max_length=20, default='', blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Группа пользоваетей"
        verbose_name_plural = "Группы пользоваетей"


class AppRating(models.Model):
    user = models.ForeignKey('analytics.FirstAnalytics', verbose_name='Пользователь', null=True,
                             on_delete=models.CASCADE)
    rating = models.PositiveIntegerField("Рейтинг (1-5)", default=0)
    comment = models.TextField("Комментарий", max_length=5000, blank=True)

    def __str__(self):
        return f'{self.user.u_id}'

    class Meta:
        verbose_name = "Рейтинг приложения"
        verbose_name_plural = "Рейтинги приложения"
