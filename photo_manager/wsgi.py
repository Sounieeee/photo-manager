"""
WSGI config for photo_manager project.
"""

import os

from django.core.wsgi import get_wsgi_application  # type: ignore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photo_manager.settings')

application = get_wsgi_application()
