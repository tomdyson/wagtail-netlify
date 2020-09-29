import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from wagtailnetlify.models import Deployment
from wagtailnetlify.management.commands.netlify import build_redirects


@csrf_exempt
def success_hook(request):
    """ Handle incoming webhook from Netlify, to record deployment completion """
    body_unicode = request.body.decode("utf-8")
    payload = json.loads(body_unicode)
    # get the first deployment without a Netlify ID
    deployment = (
        Deployment.objects.filter(netlify_id__isnull=True).order_by("id").first()
    )
    deployment.netlify_id = payload["id"]
    deployment.url = payload["url"]
    deployment.deployment_url = payload["deploy_ssl_url"]
    deployment.datetime_finished = timezone.now()
    deployment.save()
    return HttpResponse("Thanks\n")


def redirects(request):
    redirects_str, count = build_redirects()
    return HttpResponse(redirects_str)
