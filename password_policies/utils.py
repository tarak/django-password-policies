from datetime import timedelta

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from password_policies.conf import settings
from password_policies.models import PasswordHistory


class PasswordCheck(object):
    "Checks if a given user needs to change his/her password."

    def __init__(self, user):
        self.user = user
        self.expiry_datetime = self.get_expiry_datetime()

    def is_required(self):
        """Checks if a given user is forced to change his/her password.

If an instance of :class:`~password_policies.models.PasswordChangeRequired`
exists the verification is successful.

:returns: ``True`` if the user needs to change his/her password,
    ``False`` otherwise.
:rtype: bool
"""
        try:
            if self.user.password_change_required:
                return True
        except ObjectDoesNotExist:
            pass
        return False

    def is_expired(self):
        """Checks if a given user's password has expired.

:returns: ``True`` if the user's password has expired,
    ``False`` otherwise.
:rtype: bool
"""
        if PasswordHistory.objects.change_required(self.user):
            return True
        return False

    def get_expiry_datetime(self):
        "Returns the date and time when the user's password has expired."
        seconds = settings.PASSWORD_DURATION_SECONDS
        return timezone.now() - timedelta(seconds=seconds)
