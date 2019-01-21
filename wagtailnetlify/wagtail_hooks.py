from django.conf import settings
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtailnetlify.models import Deployment


class DeploymentPermissionHelper(PermissionHelper):
    # remove the add Deployment button
    def user_can_create(self, user):
        return False

    def user_can_edit_obj(self, user, obj):
        return False


class DeploymentAdmin(ModelAdmin):
    model = Deployment
    menu_icon = 'success'
    menu_order = 0
    add_to_settings_menu = True
    exclude_from_explorer = False
    list_display = ('datetime_started', 'datetime_finished', 'deployment_url', 'url')
    list_filter = ('datetime_started',)
    inspect_view_enabled=True
    permission_helper_class = DeploymentPermissionHelper


if 'wagtail.contrib.modeladmin' in settings.INSTALLED_APPS:
    modeladmin_register(DeploymentAdmin)
