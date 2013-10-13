from django.db import models
from django.utils.translation import ugettext_lazy as _

from password_policies.conf import settings
from password_policies.managers import PasswordHistoryManager


class PasswordChangeRequired(models.Model):
    """
Stores an entry to enforce password changes, related to :model:`auth.User`.

Has the following fields:
"""
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name=_('created'), db_index=True,
                                   help_text=_('The date the entry was '
                                               'created.'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                verbose_name=_('user'),
                                help_text=_('The user who needs to change '
                                            'his/her password.'),
                                related_name='password_change_required')

    class Meta:
        get_latest_by = 'created'
        ordering = ['-created']
        verbose_name = _('enforced password change')
        verbose_name_plural = _('enforced password changes')


class PasswordHistory(models.Model):
    """
Stores a single password history entry, related to :model:`auth.User`.

Has the following fields:
"""
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name=_('created'), db_index=True,
                                   help_text=_('The date the entry was '
                                               'created.'))
    password = models.CharField(max_length=128, verbose_name=_('password'),
                                help_text=_('The encrypted password.'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'),
                             help_text=_('The user this password history '
                                         'entry belongs to.'),
                             related_name='password_history_entries')

    objects = PasswordHistoryManager()

    class Meta:
        get_latest_by = 'created'
        ordering = ['-created']
        verbose_name = _('password history entry')
        verbose_name_plural = _('password history entries')
