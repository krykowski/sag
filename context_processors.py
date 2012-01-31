from django.conf import settings # import the settings file

def settings_context(context):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {
            'STATIC_URL': settings.STATIC_URL
    }