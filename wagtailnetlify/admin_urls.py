from django.conf.urls import url
from wagtailnetlify.views import list_deploys, do_deploy

urlpatterns = [
    url(r"^deployments$", list_deploys, name="list_deploys"),
    url(r"^deployments/create$", do_deploy, name="do_deploy"),
]
