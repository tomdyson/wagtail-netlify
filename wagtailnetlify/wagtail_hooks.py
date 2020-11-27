from wagtail.core import hooks
from wagtail.admin.menu import AdminOnlyMenuItem
from django.urls import include, reverse, path

from . import admin_urls


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path(r"netlify/", include(admin_urls)),
    ]


@hooks.register("register_admin_menu_item")
def register_netlify_menu_item():
    return AdminOnlyMenuItem(
        "Netlify",
        reverse("list_deploys"),
        classnames="icon icon-collapse-down",
        order=1000,
    )