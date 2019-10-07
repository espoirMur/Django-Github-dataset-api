from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic.base import RedirectView
from RestAPI.views import delete_all_events, GetPostEventView

urlpatterns = [
    # Dummy route. Can be removed.
    url('admin/', admin.site.urls),
    url('erase/', delete_all_events, name='delete-all'),
    url('events/', GetPostEventView.as_view(), name='get-all-events')
]

urlpatterns = format_suffix_patterns(urlpatterns)
