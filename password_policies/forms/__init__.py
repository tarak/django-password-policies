from __future__ import unicode_literals

from django import forms
from django.contrib.auth.hashers import is_password_usable
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.core import signing
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader

try:
    # SortedDict is deprecated as of Django 1.7 and will be removed in Django 1.9.
    # https://code.djangoproject.com/wiki/SortedDict
    from collections import OrderedDict as SortedDict
except ImportError:
    from django.utils.datastructures import SortedDict


try:
    from django.contrib.sites.models import get_current_site
except ImportError:
    from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.translation import ugettext_lazy as _

from password_policies.conf import settings
from password_policies.forms.fields import PasswordPoliciesField
from password_policies.models import PasswordHistory
from password_policies.models import PasswordChangeRequired


class PasswordPoliciesForm(forms.Form):
    """
A form that lets a user set his/her password without entering the
old password.

Has the following fields and methods:
"""
    #: This forms error messages.
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'password_used': _("The new password was used before. "
                           "Please enter another one."),
    }
    new_password1 = PasswordPoliciesField(label=_("New password"),
                                          max_length=settings.PASSWORD_MAX_LENGTH,
                                          min_length=settings.PASSWORD_MIN_LENGTH)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        """
Initializes the form.

:arg user: A :class:`~django.contrib.auth.models.User` instance.
"""
        self.user = user
        super(PasswordPoliciesForm, self).__init__(*args, **kwargs)

    def clean_new_password1(self):
        """
Validates that a given password was not used before.
"""
        new_password1 = self.cleaned_data.get('new_password1')
        if settings.PASSWORD_USE_HISTORY:
            if self.user.check_password(new_password1):
                raise forms.ValidationError(
                    self.error_messages['password_used'])
            if not PasswordHistory.objects.check_password(self.user,
                                                          new_password1):
                raise forms.ValidationError(
                    self.error_messages['password_used'])
        return new_password1

    def clean_new_password2(self):
        """
Validates that the two new passwords match.
"""
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        """
Sets the user's password to the new one and creates an entry
in the user's password history,
if :py:attr:`~password_policies.conf.Settings.PASSWORD_USE_HISTORY`
is set to ``True``.
"""
        new_password = self.cleaned_data['new_password1']
        self.user.set_password(new_password)
        if commit:
            self.user.save()
            if settings.PASSWORD_USE_HISTORY:
                password = make_password(new_password)
                PasswordHistory.objects.create(password=password, user=self.user)
                PasswordHistory.objects.delete_expired(self.user)
            PasswordChangeRequired.objects.filter(user=self.user).delete()
        return self.user


class PasswordPoliciesChangeForm(PasswordPoliciesForm):
    """
A form that lets a user change his/her password by entering
their old password.

Has the following fields and methods:
"""
    #: This forms error messages.
    error_messages = dict(PasswordPoliciesForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
        'password_similar': _("The old and the new password are too similar."),
        'password_identical': _("The old and the new password are the same."),
    })
    old_password = forms.CharField(label=_("Old password"),
                                   widget=forms.PasswordInput)

    def clean_old_password(self):
        """
Validates the current password.
"""
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'])
        return old_password

    def clean(self):
        """
Validates that old and new password are not too similar.
"""
        cleaned_data = super(PasswordPoliciesChangeForm, self).clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")

        if old_password and new_password1:
            if old_password == new_password1 and not settings.PASSWORD_USE_HISTORY:
                raise forms.ValidationError(self.error_messages['password_identical'])
            else:
                if settings.PASSWORD_DIFFERENCE_DISTANCE:
                    try:
                        import Levenshtein
                    except ImportError:
                        pass
                    else:
                        distance = Levenshtein.distance(old_password,
                                                        new_password1)
                        if distance < settings.PASSWORD_DIFFERENCE_DISTANCE:
                            raise forms.ValidationError(self.error_messages['password_similar'])
        return cleaned_data

    def save(self, commit=True):
        user = super(PasswordPoliciesChangeForm, self).save(commit=commit)
        try:
            # Checking the object id to prevent AssertionError id is None when deleting.
            if user.password_change_required and user.password_change_required.id:
                user.password_change_required.delete()
        except ObjectDoesNotExist:
            pass
        return user

PasswordPoliciesChangeForm.base_fields = SortedDict([
    (k, PasswordPoliciesChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
])


class PasswordResetForm(forms.Form):
    """
A form to let a user reset his/her password.

Has the following fields and methods:
"""
    #: This forms error messages.
    error_messages = {
        'unknown': _("That e-mail address doesn't have an associated "
                     "user account. Are you sure you've registered?"),
        'unusable': _("The user account associated with this e-mail "
                      "address cannot reset the password."),
    }
    # TODO: Help text?
    email = forms.EmailField(label=_("E-mail"), max_length=75, help_text='help')

    def clean_email(self):
        """
Validates that an active user exists with the given email address.
"""
        email = self.cleaned_data["email"]
        self.users_cache = get_user_model().objects.filter(email__iexact=email, is_active=True)
        if not len(self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])
        if any(not is_password_usable(user.password)
               for user in self.users_cache):
            raise forms.ValidationError(self.error_messages['unusable'])
        return email

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.txt',
             email_html_template_name='registration/password_reset_email.html',
             use_https=False, from_email=None, request=None):
        """
Generates a one-use only link for resetting password and sends to the
user.

:arg str domain_override: A string that changes the site name and
    domain if needed.
:arg str email_template_name: A relative path to a template in the root of a
    template directory to generate the body of the mail.
:arg str email_html_template_name: A relative path to a template in the root of
    a template directory to generate the HTML attachment of the mail.
:arg str from_email: The email address to use as sender of the email.
:arg request: A HttpRequest instance.
:arg str subject_template_name: A relative path to a template in the root of
    a template directory to generate the subject of the mail.
:arg bool use_https: Determines wether to use HTTPS while generating
    the one-use only link for resetting passwords.
"""
        from django.core.mail import EmailMultiAlternatives
        context = self.get_context_data(request,
                                        domain_override,
                                        use_https)
        signer = signing.TimestampSigner()
        for user in self.users_cache:
            c = context
            var = signer.sign(user.password)
            var = var.split(':')
            c['email'] = user.email
            c['signature'] = var[2]
            c['timestamp'] = var[1]
            c['uid'] = urlsafe_base64_encode(force_bytes(user.id))
            c['user'] = user
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            html = loader.render_to_string(email_html_template_name, c)
            msg = EmailMultiAlternatives(subject, email, from_email, [user.email])
            msg.attach_alternative(html, "text/html")
            msg.send()

    def get_context_data(self, request, domain_override, use_https):
        """
Returns a dictionary with common context items.

:arg request: A HttpRequest instance.
:arg str domain_override: A string that changes the site name and
  domain if needed.
:arg bool use_https: Determines wether to use HTTPS while generating
  the one-use only link for resetting passwords.
"""
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        context = {
            'domain': domain,
            'site_name': site_name,
            'protocol': use_https and 'https' or 'http',
        }
        return context


class PasswordPoliciesRegistrationForm(forms.Form):
    """
A form to support user registration with password policies.

Has the following fields and methods:
"""
    #: This forms error messages.
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
                                regex=r'^[\w.@+-]+$',
                                help_text=_("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
                                error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")}
                                )
    password1 = PasswordPoliciesField(label=_("Password"),
                                      max_length=settings.PASSWORD_MAX_LENGTH,
                                      min_length=settings.PASSWORD_MIN_LENGTH)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    def clean_username(self):
        """
Validates that the username is not already taken.
"""
        username = self.cleaned_data["username"]
        if username and not get_user_model().objects.filter(username__iexact=username).count():
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        """
Validates that the two passwords are identical.
"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2
