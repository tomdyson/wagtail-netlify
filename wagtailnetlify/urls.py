from django.conf.urls import url
from wagtailnetlify.views import success_hook

urlpatterns = [
    url(r'^success$', success_hook, name='success_hook'),
]