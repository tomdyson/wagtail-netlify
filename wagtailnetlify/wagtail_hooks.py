from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.helpers import ButtonHelper, PermissionHelper
from wagtailnetlify.models import Deployment


class NoAddPermissionHelper(PermissionHelper):
    # remove the add Deployment button
    def user_can_create(self, user):
        return False

class NoEditButtonHelper(ButtonHelper):
    # remove the edit button from the listing
    def get_buttons_for_obj(self, obj, exclude=[], classnames_add=[],
                            classnames_exclude=[]):
        btns = super(NoEditButtonHelper, self).get_buttons_for_obj(obj)
        return [btn for btn in btns if btn['label'] != u'Edit']

class DeploymentAdmin(ModelAdmin):
    model = Deployment
    menu_icon = 'success'  
    menu_order = 0 
    add_to_settings_menu = True
    exclude_from_explorer = False
    list_display = ('datetime_started', 'datetime_finished', 'deployment_url', 'url')
    list_filter = ('datetime_started',)
    inspect_view_enabled=True
    button_helper_class = NoEditButtonHelper
    permission_helper_class = NoAddPermissionHelper

modeladmin_register(DeploymentAdmin)
