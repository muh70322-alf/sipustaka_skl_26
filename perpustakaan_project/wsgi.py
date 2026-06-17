"""
WSGI config for perpustakaan_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Ini untuk PythonAnywhere
path = '/home/muhammadirkhamfajri/sipustaka_skl_26'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'perpustakaan_project.settings')

application = get_wsgi_application()
