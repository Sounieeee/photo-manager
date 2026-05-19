"""
ASGI config for photo_manager project.
"""

import os

from django.core.asgi import get_asgi_application  # type: ignore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photo_manager.settings')

application = get_asgi_application()
