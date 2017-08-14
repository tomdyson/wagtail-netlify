from threading import Thread
from django.core.management import call_command
from django.db import connection
from django.conf import settings
from wagtail.wagtailcore.signals import page_published


def postpone(function):
    """ cheap aysnc, see https://stackoverflow.com/a/28913218 """
    def decorator(*args, **kwargs):
        t = Thread(target = function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator

@postpone
def deploy(sender, **kwargs):
    """ build static pages, then send incremental changes to netlify """
    call_command('build')
    call_command('netlify')
    connection.close()

if hasattr(settings, 'NETLIFY_AUTO_DEPLOY') and settings.NETLIFY_AUTO_DEPLOY == False:
    pass
else:
    page_published.connect(deploy)
