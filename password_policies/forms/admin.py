from django import forms
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.utils.translation import ugettext_lazy as _

from password_policies.conf import settings
from password_policies.forms.fields import PasswordPoliciesField
from password_policies.models import PasswordHistory
from password_policies.models import PasswordChangeRequired


class PasswordPoliciesAdminForm(AdminPasswordChangeForm):
    """Enforces password policies in the admin interface.

Use this form to enforce strong passwords in the admin interface.
"""
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'password_used': _("The new password was used before. Please enter another one.")
    }

    password1 = PasswordPoliciesField(label=_("Password new"),
                                      max_length=settings.PASSWORD_MAX_LENGTH,
                                      min_length=settings.PASSWORD_MIN_LENGTH
                                      )

    def clean_password1(self):
        """
Validates that a given password was not used before.
"""
        password1 = self.cleaned_data.get('password1')
        if settings.PASSWORD_USE_HISTORY:
            if self.user.check_password(password1):
                raise forms.ValidationError(
                    self.error_messages['password_used'])
            if not PasswordHistory.objects.check_password(self.user,
                                                          password1):
                raise forms.ValidationError(
                    self.error_messages['password_used'])
        return password1


class ForceChangeAdminForm(PasswordPoliciesAdminForm):
    change_required = forms.BooleanField(initial=True, required=False, label=_('Must change?'))

    def save(self, commit=True):
        user = super(ForceChangeAdminForm, self).save(commit=commit)
        if self.cleaned_data["change_required"] and not PasswordChangeRequired.objects.filter(user=user).count():
            PasswordChangeRequired.objects.create(user=user)
        return user


class ForceChangeRequiredAdminForm(PasswordPoliciesAdminForm):

    def save(self, commit=True):
        user = super(ForceChangeRequiredAdminForm, self).save(commit=commit)
        if not PasswordChangeRequired.objects.filter(user=user).count():
            PasswordChangeRequired.objects.create(user=user)
        return user
