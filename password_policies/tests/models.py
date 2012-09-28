from django.contrib.auth.models import User
from django.utils.encoding import force_unicode

from password_policies.conf import settings
from password_policies.models import PasswordHistory
from password_policies.tests.lib import BaseTest


class PasswordHistoryModelTestCase(BaseTest):
    fixtures = ['django_password_policies_test_models_fixtures.json']

    def test_password_history_expiration_with_offset(self):
        user = User.objects.get(username='alice')
        offset = settings.PASSWORD_HISTORY_COUNT + 10
        PasswordHistory.objects.delete_expired(user, offset=offset)
        count = PasswordHistory.objects.filter(user=user).count()
        self.assertEqual(count, offset)

    def test_password_history_expiration(self):
        user = User.objects.get(username='alice')
        PasswordHistory.objects.delete_expired(user)
        count = PasswordHistory.objects.filter(user=user).count()
        self.assertEqual(count, settings.PASSWORD_HISTORY_COUNT)

    def test_password_history_recent_passwords(self):
        user = User.objects.get(username='alice')
        self.failIf(PasswordHistory.objects.check_password(user, 'Oor0ohf4bi-'))
