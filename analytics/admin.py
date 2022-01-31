from django.contrib import admin
from django.contrib.admin.models import LogEntry
from analytics.models import BannerAnalytics, EventAnalytics, FirstAnalytics
from zolatv.settings import DJANGO_ADMIN_LOGS_DELETABLE, DJANGO_ADMIN_LOGS_ENABLED
from django.utils.html import format_html


class LogEntryAdmin(admin.ModelAdmin):
    """Log Entry admin interface."""
    date_hierarchy = 'action_time'
    fields = (
        'action_time', 'user', 'content_type', 'object_id',
        'object_repr', 'action_flag', 'change_message',
    )
    list_display = (
        'action_time', 'user', 'action_message', 'content_type', 'object_link',
    )
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        'action_flag', 'content_type',
    )
    search_fields = (
        'object_repr', 'change_message',
    )

    def object_link(self, obj):
        """Returns the admin link to the log entry object if it exists."""
        admin_url = None if obj.is_deletion() else obj.get_admin_url()
        if admin_url:
            return format_html('<a href="{}">{}</a>', admin_url, obj.object_repr)
        else:
            return obj.object_repr
    object_link.short_description = 'object'

    def action_message(self, obj):
        """
        Returns the action message.
        Note: this handles deletions which don't return a change message.
        """
        change_message = obj.get_change_message()
        # If there is no change message then use the action flag label
        if not change_message:
            change_message = '{}.'.format(obj.get_action_flag_display())
        return change_message
    action_message.short_description = 'action'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('content_type')

    def has_add_permission(self, request):
        """Log entries cannot be added manually."""
        return False

    def has_change_permission(self, request, obj=None):
        """Log entries cannot be changed."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Log entries can only be deleted when the setting is enabled."""
        return DJANGO_ADMIN_LOGS_DELETABLE and super().has_delete_permission(request, obj)

    # Prevent changes to log entries creating their own log entries!
    def log_addition(self, request, object, message):
        pass

    def log_change(self, request, object, message):
        pass

    def log_deletion(self, request, object, object_repr):
        pass


# Register the LogEntry admin if enabled
if DJANGO_ADMIN_LOGS_ENABLED:
    admin.site.register(LogEntry, LogEntryAdmin)

class BannerAnalyticsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Event', {'fields': ('type', 'url', 'content_type', 'object_id', 'datetime')}),
        ('User Info', {'fields': ('user_agent', 'accept_language', 'ip', 'country')}),
    )
    readonly_fields = ('type', 'url')
    list_display = ('type', 'content_object', 'url', 'ip', 'country')
    search_fields = ('ip',)
    ordering = ('type', 'url', 'country')


admin.site.register(BannerAnalytics, BannerAnalyticsAdmin)


class EventAnalyticsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Event', {'fields': ('type', 'url', 'datetime')}),
        ('User Info', {'fields': ('user_agent', 'accept_language', 'ip', 'country')}),
    )
    readonly_fields = ('type', 'url')
    list_display = ('type', 'url', 'ip', 'country')
    search_fields = ('ip',)
    ordering = ('type', 'url', 'country')


admin.site.register(EventAnalytics, EventAnalyticsAdmin)


class FirstAnalyticsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Event', {'fields': ('u_id', 'a_id', 'url', 'datetime')}),
        ('User Info', {'fields': ('user_agent', 'accept_language', 'ip', 'country')}),
    )
    readonly_fields = ('url', 'u_id', 'a_id',)
    list_display = ('u_id', 'a_id', 'ip', 'url', 'country')
    search_fields = ('a_id',)
    ordering = ('url', 'country')


admin.site.register(FirstAnalytics, FirstAnalyticsAdmin)
