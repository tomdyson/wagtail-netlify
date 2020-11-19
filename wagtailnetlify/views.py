from django.http import HttpResponse
from django.shortcuts import render, redirect
from wagtailnetlify.management.commands.netlify import build_redirects
from .utils import netlify_deploys
from .models import deploy


def redirects(request):
    redirects_str, count = build_redirects()
    return HttpResponse(redirects_str)


def list_deploys(request):
    deploys = netlify_deploys()
    return render(
        request,
        "wagtailnetlify/deploy_listing.html",
        {"deploys": deploys},
    )


def do_deploy(request):
    deploy()  # non-async deploy
    return redirect(list_deploys)