from django.conf.urls import url
from wagtailnetlify.views import redirects

urlpatterns = [url(r"^redirects$", redirects, name="redirect_builder")]
