from django.test import TestCase

from password_policies.conf import settings


class BaseTest(TestCase):

    def setUp(self):
        """
        Isolate all application specific settings.
        """
        output = super(BaseTest, self).setUp()
        settings.isolated = True
        return output

    def tearDown(self):
        """
        Restore settings to their original state.
        """
        settings.isolated = False
        settings.revert()
        return super(BaseTest, self).tearDown()
