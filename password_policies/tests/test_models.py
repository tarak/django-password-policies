from password_policies.conf import settings
from password_policies.models import PasswordHistory
from password_policies.tests.lib import BaseTest
from password_policies.tests.lib import create_user
from password_policies.tests.lib import create_password_history
from password_policies.tests.lib import passwords


class PasswordHistoryModelTestCase(BaseTest):

    def setUp(self):
        self.user = create_user()
        create_password_history(self.user)
        return super(PasswordHistoryModelTestCase, self).setUp()

    def test_password_history_expiration_with_offset(self):
        offset = settings.PASSWORD_HISTORY_COUNT + 2
        PasswordHistory.objects.delete_expired(self.user, offset=offset)
        count = PasswordHistory.objects.filter(user=self.user).count()
        self.assertEqual(count, offset)

    def test_password_history_expiration(self):
        PasswordHistory.objects.delete_expired(self.user)
        count = PasswordHistory.objects.filter(user=self.user).count()
        self.assertEqual(count, settings.PASSWORD_HISTORY_COUNT)

    def test_password_history_recent_passwords(self):
        self.failIf(PasswordHistory.objects.check_password(self.user,
                                                           passwords[-1]))
