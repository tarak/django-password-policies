from datetime import datetime
from datetime import timedelta

from django.utils import timezone
from django.core.urlresolvers import resolve, reverse, NoReverseMatch, Resolver404
from django.http import HttpResponseRedirect

from password_policies.conf import settings
from password_policies.models import PasswordHistory

import re

class PasswordChangeMiddleware(object):
    """
A middleware to force a password change.

If a password history exists the last change of password
can easily be determined by just getting the newest entry.
If the user has no password history it is assumed that the
password was last changed when the user has or was registered.

.. note::
    This only works on a GET HTTP method. Redirections on a
    HTTP POST are tricky, so the risk of messing up a POST
    is not taken...

To use this middleware you need to add it to the
``MIDDLEWARE_CLASSES`` list in a project's settings::

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'password_policies.middleware.PasswordChangeMiddleware',
        # ... other middlewares ...
    )

.. note::
    The order of this middleware in the stack is important,
    it must be listed after the authentication AND the session
    middlewares.

.. warning::
    This middleware does not try to redirect using the HTTPS
    protocol.
"""

    checked = '_password_policies_last_checked'
    expired = '_password_policies_expired'
    last = '_password_policies_last_changed'
    required = '_password_policies_change_required'

    def _check(self, request):
        if not request.session.get(self.last, None):
            newest = PasswordHistory.objects.get_newest(request.user)
            if newest:
                request.session[self.last] = newest.created
            else:
                request.session[self.last] = request.user.date_joined
        d = timedelta(seconds=settings.PASSWORD_DURATION_SECONDS)
        expired_date = self.now - d
        request.session[self.expired] = expired_date
        if request.session[self.last] < request.session[self.expired]:
            request.session[self.required] = True
        else:
            request.session[self.required] = False

    def _check_necessary(self, request):
        if not request.session.get(self.checked, None):
            request.session[self.checked] = self.now
        seconds = settings.PASSWORD_CHECK_SECONDS
        d = timedelta(seconds=seconds)
        if request.session[self.checked] < self.now - d:
            try:
                del request.session[self.last]
                del request.session[self.checked]
                del request.session[self.required]
                del request.session[self.expired]
            except KeyError:
                pass

    def _is_excluded_path(self, actual_path):
        paths = settings.PASSWORD_CHANGE_MIDDLEWARE_EXCLUDED_PATHS
        path = r'^%s$' % self.url
        paths.append(path)
        media_url = settings.MEDIA_URL
        if media_url:
            paths.append(r'^%s?' % media_url)
        static_url = settings.STATIC_URL
        if static_url:
            paths.append(r'^%s?' % static_url)
        if settings.PASSWORD_CHANGE_MIDDLEWARE_ALLOW_LOGOUT:
            try:
                logout_url = reverse('logout')
            except NoReverseMatch:
                pass
            else:
                paths.append(r'^%s$' % logout_url)
            try:
                logout_url = resolve(u'/admin/logout/')
            except Resolver404:
                pass
            else:
                paths.append(r'^%s$' % logout_url)
        for path in paths:
            if re.match(path, actual_path):
                return True
        return False

    def _redirect(self, request):
        if request.session[self.required]:
            redirect_to = request.GET.get(settings.REDIRECT_FIELD_NAME, '')
            if redirect_to:
                next = redirect_to
            else:
                next = request.get_full_path()
            url = "%s?%s=%s" % (self.url, settings.REDIRECT_FIELD_NAME, next)
            return HttpResponseRedirect(url)

    def process_request(self, request):
        if request.method != 'GET':
            return
        try:
            resolve(request.path)
        except Resolver404:
            return
        self.now = timezone.now()
        self.url = reverse('password_change')
        if settings.PASSWORD_DURATION_SECONDS and \
                request.user.is_authenticated() and \
                not self._is_excluded_path(request.path):
            self._check_necessary(request)
            self._check(request)
            return self._redirect(request)
