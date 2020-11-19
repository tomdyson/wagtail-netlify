import os
import subprocess
import requests
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

try:
    from wagtail.contrib.redirects.models import Redirect
except ImportError:  # Wagtail < 2.0
    from wagtail.wagtailredirects.models import Redirect


def build_redirects():
    out = "# Redirects from what the browser requests to what we serve\n"
    count = 0
    for redirect in Redirect.objects.all():
        status_code = "302"
        if redirect.is_permanent:
            status_code = "301"
        out += "%s\t%s\t%s\n" % (redirect.old_path, redirect.link, status_code)
        count += 1
    return out, count


class Command(BaseCommand):

    help = "Deploys your site to Netlify, or triggers a build"

    def write_redirects(self):
        """Redirects are configured in a file called '_redirects'
        at the root of the build directory
        """
        if not hasattr(settings, "BUILD_DIR"):
            raise CommandError("BUILD_DIR is not defined in settings")
        redirect_file = os.path.join(settings.BUILD_DIR, "_redirects")
        redirects_str, count = build_redirects()
        with open(redirect_file, "w") as fo:
            fo.write(redirects_str)
        self.stdout.write("Written %s redirect(s)" % (count))

    def trigger_build(self):
        """
        Trigger a Netlify build using build hooks
        https://docs.netlify.com/configure-builds/build-hooks/
        """
        netlify_build_hook = getattr(settings, "NETLIFY_BUILD_HOOK", None)
        if not netlify_build_hook:
            raise CommandError("NETLIFY_BUILD_HOOK is not defined in settings")
        requests.post(url=netlify_build_hook)
        self.stdout.write("Netlify build triggered")

    def deploy(self):
        """
        Deploy the contents of `BUILD_DIR` to Netlify,
        using `NETLIFY_SITE_ID` and `NETLIFY_API_TOKEN` if available.
        """

        netlify_cli = getattr(settings, "NETLIFY_PATH", None)
        if not netlify_cli:
            raise CommandError("NETLIFY_PATH is not defined in settings")

        command = [
            netlify_cli,
            "deploy",
            "--dir={}".format(settings.BUILD_DIR),
            "--prod",
            '--message="Wagtail Deployment #{}"'.format(deployment.pk),
        ]

        site_id = getattr(settings, "NETLIFY_SITE_ID", None)
        if site_id:
            command.append("--site={}".format(site_id))

        auth_token = getattr(settings, "NETLIFY_API_TOKEN", None)
        if auth_token:
            command.append("--auth={}".format(auth_token))

        subprocess.call(command)

    def add_arguments(self, parser):
        parser.add_argument(
            "-n", "--no-deploy", action="store_true", help="Do not deploy"
        )
        parser.add_argument(
            "-t",
            "--trigger-build",
            action="store_true",
            help="Trigger build on Netlify",
        )

    def handle(self, *args, **kwargs):
        trigger = kwargs["trigger_build"]
        if trigger:
            self.trigger_build()
        else:
            self.write_redirects()
            no_deploy = kwargs["no_deploy"]
            if not no_deploy:
                self.deploy()
