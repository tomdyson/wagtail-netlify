from threading import Thread
from django.db import models
from django.core.management import call_command
from django.db import connection
from django.conf import settings
from django.utils.module_loading import import_string

try:
    from wagtail.wagtailcore.signals import page_published
except ImportError:  # Wagtail < 2.0
    from wagtail.core.signals import page_published


class Deployment(models.Model):
    netlify_id = models.CharField(max_length=30, null=True)
    url = models.URLField(null=True)
    deployment_url = models.URLField(null=True)
    datetime_started = models.DateTimeField(auto_now_add=True, help_text='deployment started')
    datetime_finished = models.DateTimeField('deployment completed', null=True)


def postpone(function):
    """
    Cheap aysnc, see https://stackoverflow.com/a/28913218
    """
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator


@postpone
def deploy(sender, **kwargs):
    """
    Build static pages, then send incremental changes to netlify.
    """
    call_command('build')
    call_command('netlify')
    connection.close()


if getattr(settings, 'NETLIFY_AUTO_DEPLOY', False) == True:
    function_path = getattr(settings, 'NETLIFY_DEPLOY_FUNCTION', 'wagtailnetlify.models.deploy')
    function = import_string(function_path)
    page_published.connect(function)
