from django import forms
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.backends import utils
from users.models import CodeActivation, UserProfile, UserWatchHisory, UserWatchList, UserFeedback, Subscription, \
    UserSubscription, Comment, CommentLike, Rating, RefLink, UserGroup, AppRating

admin.site.site_header = "ZolaTV"
admin.site.index_title = "Admin panel"
admin.site.site_title = "ZolaTV"

UserModel = get_user_model()


class CodeActivationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'code')}),
    )
    readonly_fields = ('user',)
    list_display = ('user', 'code')
    search_fields = ('user', 'code')
    ordering = ('user', 'code')


admin.site.register(CodeActivation, CodeActivationAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    def get_date_joined(self, obj):
        return obj.user.date_joined.strftime("%d.%m.%Y, %H:%M:%S")

    get_date_joined.short_description = ugettext_lazy("Register date")
    fieldsets = (
        (None, {'fields': ('name', 'user')}),
        ('Private Information', {'fields': ('gender', 'age')}),
        ('Lists', {'fields': ('genres', 'kinds')}),
        ('Settings', {'fields': ('dark_mode', 'ad_free_time', 'get_date_joined')}),
    )
    readonly_fields = ('user','get_date_joined')
    list_display = ('id', 'name', 'user', 'gender', 'age', 'ad_free_time', 'get_date_joined')
    search_fields = ('name', 'user', 'gender', 'age')
    ordering = ('id', 'name', 'user', 'gender', 'age', 'ad_free_time')


admin.site.register(UserProfile, UserProfileAdmin)


# class UserCreationForm(forms.ModelForm):
#     """A form for creating new users. Includes all the required
#     fields, plus a repeated password."""
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
#
#     class Meta:
#         model = UserModel
#         fields = ('loginuser', 'gender', 'is_email', 'is_active')
#
#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise ValidationError("Passwords don't match")
#         return password2
#
#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
#
#
# class UserChangeForm(forms.ModelForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     disabled password hash display field.
#     """
#     password = ReadOnlyPasswordHashField()
#
#     class Meta:
#         model = UserModel
#         fields = ('loginuser', 'is_email', 'password', 'is_active', 'is_admin')


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active', 'is_activated', 'is_adm', ('groups', 'user_permissions'))}),
        ('Private', {'fields': ('date_joined', 'last_login', 'ip', 'last_login_ip')})
    )
    list_display = ('email', 'phone', 'is_superuser', 'is_activated', 'is_active', 'is_adm')
    list_filter = ('is_superuser',)
    filter_horizontal = ('groups', 'user_permissions')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2', 'is_superuser'),
        }),
    )
    search_fields = ('email', 'phone')
    ordering = ('email', 'phone', 'is_superuser')
    readonly_fields = ('last_login_ip', 'ip')


admin.site.register(UserModel, UserAdmin)


class UserWatchHistoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'content_type', 'object_id', 'date')}),
    )
    list_display = ('user', 'content_object', 'object_id', 'date')
    readonly_fields = ('user', 'object_id', 'content_type', 'date')


admin.site.register(UserWatchHisory, UserWatchHistoryAdmin)


class UserWatchListAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'content_type', 'object_id', 'date')}),
    )
    list_display = ('user', 'content_object', 'object_id', 'date')
    readonly_fields = ('user', 'object_id', 'content_type', 'date')


admin.site.register(UserWatchList, UserWatchListAdmin)


class UserFeedbackAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'text', 'date')}),
    )
    list_display = ('user', 'date')
    readonly_fields = ('user', 'date')


admin.site.register(UserFeedback, UserFeedbackAdmin)


class SubAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'price', 'discount_price', 'term', 'economy', 'show_economy')}),
    )
    list_display = ('name', 'term', 'price')


admin.site.register(Subscription, SubAdmin)


class UserSubAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'subscription', 'date_begin')}),
    )
    list_display = ('user', 'subscription', 'date_begin')
    # readonly_fields = ('user',)


admin.site.register(UserSubscription, UserSubAdmin)


class CommentsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'text', 'content_type', 'object_id', 'date')}),
    )
    list_display = ('content_object', 'user', 'date')
    readonly_fields = ('user', 'date')


admin.site.register(Comment, CommentsAdmin)


class CommentLikeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'comment')}),
    )
    list_display = ('user', 'comment')
    readonly_fields = ('user',)


admin.site.register(CommentLike, CommentLikeAdmin)


class RatingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'grade', 'content_type', 'object_id', 'date')}),
    )
    list_display = ('user', 'content_object', 'grade')
    readonly_fields = ('user', 'grade', 'date')


admin.site.register(Rating, RatingAdmin)


class RefLinkAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'link', 'clicks', 'downloads', 'date')}),
    )
    list_display = ('user', 'link', 'clicks', 'downloads')
    readonly_fields = ('user', 'date')


admin.site.register(RefLink, RefLinkAdmin)


class UserGroupAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'type', 'value', 'users')}),
        ("Info", {'fields': (('age', 'age_to'), 'gender', 'location', 'target')}),
    )
    list_display = ('name', 'type')


admin.site.register(UserGroup, UserGroupAdmin)


class AppRatingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'rating', 'comment')}),
    )
    list_display = ('user', 'rating')
    readonly_fields = ('user',)


admin.site.register(AppRating, AppRatingAdmin)
