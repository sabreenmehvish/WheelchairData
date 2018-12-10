"""
WSGI config for redditdata project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import django
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redditdata.settings')
sys.path.append('/var/www/html/redditdata')
sys.path.append('/var/www/html/redditdata/redditdata')
application = get_wsgi_application()
