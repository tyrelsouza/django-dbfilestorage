from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^dbfilestorage/', include('dbfilestorage.urls')),
]
