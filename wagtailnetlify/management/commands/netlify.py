import os
import subprocess
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from wagtailnetlify.models import Deployment

try:
    from wagtail.contrib.redirects.models import Redirect
except ImportError:  # Wagtail < 2.0
    from wagtail.wagtailredirects.models import Redirect


class Command(BaseCommand):

    help = "Deploys your baked Wagtail site to Netlify"

    def build_redirects(self):
        # Redirects are configured in a file called '_redirects' at the root of the build directory
        if not hasattr(settings, "BUILD_DIR"):
            raise CommandError("BUILD_DIR is not defined in settings")
        redirect_file = os.path.join(settings.BUILD_DIR, "_redirects")
        fo = open(redirect_file, "w")
        fo.write("# Redirects from what the browser requests to what we serve\n")
        # for each redirect, write old path, new url, status code
        count = 0
        for redirect in Redirect.objects.all():
            status_code = "302"
            if redirect.is_permanent:
                status_code = "301"
            fo.write("%s\t%s\t%s\n" % (redirect.old_path, redirect.link, status_code))
            count += 1
        fo.close()
        self.stdout.write("Written %s redirect(s) to %s" % (count, redirect_file))

    def deploy(self):
        """
        Deploy the contents of `BUILD_DIR` to Netlify,
        using `NETLIFY_SITE_ID` and `NETLIFY_API_TOKEN` if available.
        """

        netlify_cli = getattr(settings, "NETLIFY_PATH", None)
        if not netlify_cli:
            raise CommandError("NETLIFY_PATH is not defined in settings")

        deployment = Deployment()
        deployment.save()

        command = [netlify_cli, "deploy"]
        command.append("--dir={}".format(settings.BUILD_DIR))
        command.append("--prod")
        command.append('--message="Wagtail Deployment #{}"'.format(deployment.pk))

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

    def handle(self, *args, **kwargs):
        no_deploy = kwargs["no_deploy"]
        self.build_redirects()
        if not no_deploy:
            self.deploy()
