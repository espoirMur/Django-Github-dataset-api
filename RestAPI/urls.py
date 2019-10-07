from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic.base import RedirectView
from RestAPI.views import (delete_all_events, GetPostEventView,
                           get_events_by_actor_id)

urlpatterns = [
    # Dummy route. Can be removed.
    url(r'^actors/(?P<actor_id>[0-9]+)/$',
        get_events_by_actor_id,
        name='get-event-by-actor'),
    url(r'^', GetPostEventView.as_view(), name='get-all-events')
]
