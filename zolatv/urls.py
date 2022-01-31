from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler400, handler403, handler404, handler500
from django.conf.urls.static import static
from django.conf import settings
from main.views import PnfView
from django.conf.urls.i18n import i18n_patterns
from analytics.views import AnalyticsPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analytics/', AnalyticsPageView.as_view(), name="analytics-page"),
    path('il8n/', include('django.conf.urls.i18n')),
    path('analyt/', include("analytics.urls"))
]

urlpatterns += i18n_patterns(
    path('', include("main.urls")),
    path('sreg/', include('social.apps.django_app.urls', namespace='social')),
)
handler404 = PnfView.as_view()
handler403 = PnfView.as_view()
handler400 = PnfView.as_view()

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
