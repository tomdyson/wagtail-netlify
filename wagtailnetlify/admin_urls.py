from django.urls import re_path
from wagtailnetlify.views import list_deploys, do_deploy

urlpatterns = [
    re_path(r"^deployments$", list_deploys, name="list_deploys"),
    re_path(r"^deployments/create$", do_deploy, name="do_deploy"),
]
