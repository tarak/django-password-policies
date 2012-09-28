from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from password_policies.managers import PasswordHistoryManager


class PasswordHistory(models.Model):
    """
    Stores a single password history entry, related to :model:`auth.User`.

    """
    password = models.CharField(max_length=128, verbose_name=_('password'))
    user = models.ForeignKey(User, verbose_name=_('user'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))

    objects = PasswordHistoryManager()

    class Meta:
        get_latest_by = 'created'
        ordering = ['-created']
        unique_together = ('password', 'user')
        verbose_name = _('password history entry')
        verbose_name_plural = _('password history entries')
