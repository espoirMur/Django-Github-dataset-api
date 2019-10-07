from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic.base import RedirectView
from RestAPI.views import delete_all_events, GetPostEventView, GetEventByActor

urlpatterns = [
    # Dummy route. Can be removed.
    url(r'^admin/', admin.site.urls),
    url(r'^erase/', delete_all_events, name='delete-all'),
    url(r'^events/', include('RestAPI.urls'))
]
