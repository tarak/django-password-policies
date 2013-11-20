from datetime import timedelta
from django.utils import timezone
from password_policies.conf import settings
from password_policies.models import PasswordChangeRequired, PasswordHistory


class PasswordCheck(object):
    "Checks if a given user needs to change his/her password."
    def __init__(self, user):
        self.user = user

    def is_required_to_change(self):
        """Checks if a given user is forced to change his/her password.

If an instance of :class:`~password_policies.models.PasswordChangeRequired`
exists the verification is successful.

:returns: ``True`` if the user needs to change his/her password,
    ``False`` otherwise.
:rtype: bool
"""
        if self.user.password_change_required.count():
            return True
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
        """Return the date and time when the user's password has expired.

If an instance of :class:`~password_policies.models.PasswordChangeRequired`
exists the verification is successful.

:returns: ``True`` if the user's password has expired,
    ``False`` otherwise.
:rtype: bool
"""
        seconds = settings.PASSWORD_DURATION_SECONDS
        return timezone.now() - timedelta(seconds=seconds)