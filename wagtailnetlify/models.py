from threading import Thread
from django.core.management import call_command
from django.db import connection
from django.conf import settings
from django.utils.module_loading import import_string

try:
    from wagtail.wagtailcore.signals import page_published
except ImportError:  # Wagtail < 2.0
    from wagtail.core.signals import page_published


def postpone(function):
    """
    Cheap aysnc, see https://stackoverflow.com/a/28913218
    """

    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    return decorator


def deploy():
    """
    Trigger a build on Netlify, if NETLIFY_BUILD_HOOK is supplied, or
    build static pages, then upload incremental changes to Netlify.
    """
    netlify_build_hook = getattr(settings, "NETLIFY_BUILD_HOOK", None)
    if netlify_build_hook:
        call_command("netlify", "--trigger-build")
    else:
        call_command("build")
        call_command("netlify")


@postpone
def async_deploy(sender, **kwargs):
    deploy()
    connection.close()


if getattr(settings, "NETLIFY_AUTO_DEPLOY", False) == True:
    function_path = getattr(
        settings, "NETLIFY_DEPLOY_FUNCTION", "wagtailnetlify.models.async_deploy"
    )
    function = import_string(function_path)
    page_published.connect(function)
