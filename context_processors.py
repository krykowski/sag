from django.conf import settings # import the settings file

from utils import current_time

def settings_context(context):
    return {
            'STATIC_URL': settings.STATIC_URL,
            'PROJECT_NAME': settings.PROJECT_NAME,
            'PROJECT_NAME_SHORT': settings.PROJECT_NAME_SHORT,
            'current_time': current_time(),
    }