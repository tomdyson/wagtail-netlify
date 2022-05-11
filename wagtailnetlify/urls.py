from django.urls import re_path
from wagtailnetlify.views import redirects

urlpatterns = [re_path(r"^redirects$", redirects, name="redirect_builder")]
