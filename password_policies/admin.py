from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from password_policies.conf import settings
from password_policies.models import PasswordHistory
from password_policies.models import PasswordChangeRequired


def force_password_change(modeladmin, request, queryset):
    for user in queryset.all():
        PasswordChangeRequired.objects.create(user=user)
force_password_change.short_description = _('Force password change for selected'
                                            ' users')


class PasswordHistoryAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    exclude = ('password',)
    list_display = ('id', 'user', 'created')
    list_display_links = ('id', 'user',)
    search_fields = settings.PASSWORD_HISTORY_ADMIN_SEARCH_FIELDS
    readonly_fields = ('user', 'created')

    def has_add_permission(self, request):
        return False


class PasswordChangeRequiredAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('id', 'user', 'created')
    list_display_links = ('id', 'user',)
    search_fields = settings.PASSWORD_CHANGE_REQUIRED_ADMIN_SEARCH_FIELDS
    readonly_fields = ('user', 'created')

    def get_readonly_fields(self, request, obj=None):
        """
Sets the ``user`` and the ``created`` field to read only if an instance
already exists.
"""
        if obj:
            return ['user']
        else:
            return []


admin.site.register(PasswordHistory, PasswordHistoryAdmin)
admin.site.register(PasswordChangeRequired, PasswordChangeRequiredAdmin)
