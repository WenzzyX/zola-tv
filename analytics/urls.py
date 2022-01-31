from django.urls import path
from analytics.views import (SaveEventView, SaveFirstView, ClearViews)

urlpatterns = [
    path('s_event', SaveEventView.as_view(), name='save-event-post'),
    path('s_first', SaveFirstView.as_view(), name="save-first-post"),
    path('clear_views', ClearViews.as_view(), name="clear-views-get"),
]
