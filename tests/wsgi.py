from __future__ import absolute_import, print_function, unicode_literals

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")

application = get_wsgi_application()
